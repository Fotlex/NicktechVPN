import uuid
import json

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import JsonResponse
from django.utils import timezone

from yookassa import Payment as YookassaPayment, Configuration
from yookassa.domain.notification import WebhookNotificationFactory

from .serializers import TariffSerializer
from .models import Tariff, Payment
from backend.core.config import config
from backend.users.models import User
from backend.servers.tasks import update_client_task
from backend.content.models import VpnSettings


Configuration.account_id = config.YOOKASSA_SHOP_ID
Configuration.secret_key = config.YOOKASSA_SECRET_KEY


class TariffViewSet(viewsets.GenericViewSet):
    queryset = Tariff.objects.filter(is_active=True)
    serializer_class = TariffSerializer
    
    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
class PaymentViewSet(viewsets.ViewSet):
    @action(detail=False, methods=['post'])
    def yookassa_create_payment(self, request):
        email = request.data.get('email')
        tariff_id = request.data.get('tariff_id')
        
        if not tariff_id or not email:
            return Response({"error": "tariff_id and email is required"}, status=status.HTTP_400_BAD_REQUEST)

        tariff = Tariff.objects.get(id=tariff_id)
        if not tariff:
            return Response({"error": "Tariff not found"}, status=status.HTTP_404_NOT_FOUND)
        
        user_id = request.tg_user.id
        customer_name = f'{request.tg_user.first_name}'
        return_url = config.APP_URL
        print("Find email in create payment:", email)

        try:
            yookassa_payment = YookassaPayment.create({
                "amount": {
                    "value": str(tariff.price),
                    "currency": "RUB"
                },
                "confirmation": {
                    "type": "redirect", 
                    "return_url": return_url
                },
                "capture": True,
                "description": f"Оплата подписки на {tariff.duration_days}",
                "metadata": {
                    "user_id": user_id,
                    "tariff_id": tariff_id
                },
                "receipt": {
                    "customer": {
                        "full_name": customer_name,
                        "email": email,
                        "phone": "+79000000000"
                    },
                    "tax_system_code": 1,
                    "items": [
                        {
                            "description": "Пополнение баланса",
                            "quantity": "1.00",
                            "amount": {"value": str(tariff.price), "currency": "RUB"},
                            "vat_code": 6,
                            "payment_subject": "service",
                            "payment_mode": "full_prepayment"
                        }
                    ],
                },
            }, idempotency_key=str(uuid.uuid4()))

            Payment.objects.create(
                payment_id = yookassa_payment.id,
                user=User.objects.get(id=user_id),
                tariff=Tariff.objects.get(id=tariff_id),
                create_at=timezone.now(),
            )
            
            return Response(
                {'payment_url': yookassa_payment.confirmation.confirmation_url},
                status=status.HTTP_200_OK
            )

        except Exception as e:
            print(e)
            return Response({"error": "error creating payment"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
class YooKassaWebhookView(viewsets.ViewSet):
    @action(detail=False, methods=['post'])
    def webhook(self, request):
        try:
            event_json = request.body.decode('utf-8')
            event_dict = json.loads(event_json)

            notification = WebhookNotificationFactory().create(event_dict)
            payment_id = notification.object.id
            
            if notification.object.status == "succeeded":
                payment = Payment.objects.select_related('user').filter(payment_id=payment_id).first()
                payment.status = "succeeded"
                user = payment.user
                tariff = payment.tariff
                vpn_settings = VpnSettings.objects.get(id=1)
                gb_limit = tariff.duration_days * vpn_settings.trafic_day_limit
                payment.save()
                
            update_client_task.apply_async(args=[
                user.id,
                tariff.duration_days,
                gb_limit,
            ])
                
            if notification.object.status == "canceled":
                payment.status = "canceled"

            return Response({"status": "ok"}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)