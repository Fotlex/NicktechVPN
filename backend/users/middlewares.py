import re

from datetime import timedelta 

from django.conf import settings
from django.http import JsonResponse
from django.utils import timezone

from rest_framework import status

from telegram_webapp_auth.auth import TelegramAuthenticator
from telegram_webapp_auth.errors import InvalidInitDataError

from .models import User, Subscription
from backend.servers.tasks import create_client_task
from backend.content.models import VpnSettings


class TWAAuthorizationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self._telegram_authenticator = TelegramAuthenticator(settings.TELEGRAM_SECRET_KEY)
        
    def __call__(self, request):
        if request.path.startswith('/admin/') or request.path.startswith('/static/') or request.path == '/api/v1/yookassa/webhook/':
            return self.get_response(request)
            
        auth_cred = request.headers.get('Authorization')
        
        if not auth_cred:
            return JsonResponse(
                data={'error': 'Authorization header required'}, 
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        try:
            init_data = self._telegram_authenticator.validate(auth_cred)
            print("correct init data")
        except InvalidInitDataError:
            print("invalid init data")
            return JsonResponse(
                data={'error': 'Invalid Telegram auth data'}, 
                status=status.HTTP_401_UNAUTHORIZED
            )

        try:
            current_user, created = User.objects.get_or_create(
                id=init_data.user.id,
                defaults={
                    'username': init_data.user.username,
                    'first_name': init_data.user.first_name,
                }
            )

            if created:
                vpn_settings = VpnSettings.objects.get(id=1)
                
                trial_end_date = timezone.now() + timedelta(days=vpn_settings.trial_time)
                
                Subscription.objects.create(
                    user=current_user,
                    end_date=trial_end_date,
                    total_bytes_limit=vpn_settings.trial_time * vpn_settings.trafic_day_limit * 1024**3,
                    trial_activated=True,
                    is_vpn_client_active=True,
                )
                
                create_client_task.apply_async(args=[
                    current_user.id,
                    vpn_settings.trial_time * vpn_settings.trafic_day_limit
                ])
                
                start_param = self.get_start_param(request)
                print("проверка start_param")
                if start_param:
                    start_param = str(start_param)
                    if start_param.isdigit():
                        referrer_id = int(start_param)
                        if current_user.tg_id != referrer_id:
                            try:
                                referrer_user = User.objects.get(id=referrer_id)
                                
                                current_user.referred_by = referrer_user
                                current_user.save()
                                
                            except Exception as e:
                                print(f"Error creating referral: {e}")
            
            request.tg_user = current_user
            return self.get_response(request)
        except Exception as e:
            print('error:', str(e))
            return JsonResponse(
                data={'error': str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            
    def get_start_param(self, request):
        try:
            return request.GET.get('start_param')
        except Exception as e:
            print("ошибка получения start_param:", e)
            return None
        