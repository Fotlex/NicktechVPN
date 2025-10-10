import uuid

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import JsonResponse
from django.utils import timezone

from yookassa import Payment as YookassaPayment, Configuration

from .serializers import TariffSerializer
from .models import Tariff, Payment
from backend.core.config import config
from backend.users.models import User


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
        