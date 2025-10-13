import base64

from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action

from backend.users.models import Subscription
from backend.servers.py3xui import get_combined_subscriptions


class SubscriptionViewSet(viewsets.ViewSet):
    @action(detail=False, methods=['get'], url_path='(?P<access_token>[^/.]+)')
    def get_subscription_link(self, request, access_token: str):
        try:
            subscription = Subscription.objects.get(vless_uuid=access_token)
            
            combined_subscriptions = get_combined_subscriptions(subscription=subscription)
            print(combined_subscriptions)

            base64_encoded = base64.b64encode("\n".join(combined_subscriptions).encode("utf-8")).decode("utf-8")

            expiry_time_seconds = int(subscription.end_date.timestamp())
            response = HttpResponse(base64_encoded, content_type="text/plain; charset=utf-8")
            response["Content-Disposition"] = "inline"
            response["profile-update-interval"] = "2"
            response["profile-title"] = "base64:TklLVEVDSCBWUE7wn4yV"
            response["subscription-userinfo"] = f"upload=0; download={subscription.used_bytes}; total={subscription.total_bytes_limit}; expire={expiry_time_seconds}"

            return response
        except Exception as e:
            print(f"Ошибка при обработке запроса: {e}")
            return HttpResponseBadRequest("Ошибка сервера")
