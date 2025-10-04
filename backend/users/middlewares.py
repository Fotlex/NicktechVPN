from datetime import timedelta 

from django.conf import settings
from django.http import JsonResponse
from django.utils import timezone

from rest_framework import status

from telegram_webapp_auth.auth import TelegramAuthenticator
from telegram_webapp_auth.errors import InvalidInitDataError

from .models import User, Subscription


class TWAAuthorizationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self._telegram_authenticator = TelegramAuthenticator(settings.TELEGRAM_SECRET_KEY)
        
    def __call__(self, request):
        if request.path.startswith('/admin/') or request.path.startswith('/static/'):
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
                trial_end_date = timezone.now() + timedelta(days=5)
                
                Subscription.objects.create(
                    user=current_user,
                    end_date=trial_end_date,
                    trial_activated=True
                )
            
            request.tg_user = current_user
            return self.get_response(request)
        except Exception as e:
            print('error:', str(e))
            return JsonResponse(
                data={'error': str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )