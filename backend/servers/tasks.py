from celery import shared_task

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
def add_client_to_server_task(user: User, server: VpnServer):
    try:
        add_client_to_server(user=user, server=server)
    except Exception as e:
        pass
    
    
@shared_task(name='auto_update_data')
def auto_update_data_task():
    try:
        subscriptions = Subscription.objects.filter(is_vpn_client_active=True)
        for subscription in subscriptions:
            auto_update_data(subscription=subscription)
    except Exception as e:
        print(e)