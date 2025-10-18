from celery import shared_task
import requests
from django.utils import timezone
from datetime import timedelta

from backend.core.config import config
from .py3xui import (
    create_client,
    update_client,
    add_client_to_server,
    User, VpnServer, Subscription,
    auto_update_data
)


@shared_task
def create_client_task(tg_id: int, limit_gb: int):
    try:
        create_client(tg_id=tg_id, limit_gb=limit_gb)
    except Exception as e:
        pass
    
    
@shared_task
def update_client_task(tg_id: int, days: int, gb_limit: int):
    try:
        update_client(tg_id=tg_id, days=days, gb_limit=gb_limit)
    except Exception as e:
        pass
    
    
@shared_task
def add_client_to_server_task(user_id: int, server_id: int):
    try:
        user = User.objects.get(id=user_id)
        server = VpnServer.objects.get(id=server_id)
        add_client_to_server(user=user, server=server)
    except Exception as e:
        print(f'Ошибка при добавлении на сервер {e}')
        pass
    
    
@shared_task(name='auto_update_data')
def auto_update_data_task():
    try:
        subscriptions = Subscription.objects.filter(is_vpn_client_active=True)
        for subscription in subscriptions:
            auto_update_data(subscription=subscription)
            
            
        for subscription in subscriptions:
            if timezone.now() + timedelta(days=2) > subscription.end_date:
                if not subscription.last_notification_update or subscription.last_notification_update + timedelta(days=1) > timezone.now():
                    user = subscription.user
                    requests.post(
                        url=f'https://api.telegram.org/bot{config.BOT_TOKEN}/sendMessage',
                        json={
                            'chat_id': user.id,
                            'text': '⚠️ Срок действия подписки подходит к концу. Не забудьте продлить ее',
                        }
                    )
                    subscription.last_notification_update = timezone.now()
                    subscription.save()
    except Exception as e:
        print(e)
        