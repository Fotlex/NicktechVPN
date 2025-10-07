from celery import shared_task

from .py3xui import create_client, update_client, add_client_to_server, User, VpnServer


@shared_task
def create_client_task(tg_id: int, limit_gb: int):
    try:
        create_client(tg_id=tg_id, limit_gb=limit_gb)
    except Exception as e:
        raise
    
    
@shared_task
def update_client_task(tg_id: int, days: int, gb_limit: int):
    try:
        update_client(tg_id=tg_id, days=days, gb_limit=gb_limit)
    except Exception as e:
        raise
    
    
@shared_task
def add_client_to_server_task(user: User, server: VpnServer):
    try:
        add_client_to_server(user=user, server=server)
    except Exception as e:
        raise