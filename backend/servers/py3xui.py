import uuid

from py3xui import Api, Client

from datetime import datetime, timedelta

from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist

from backend.users.models import User, Subscription
from backend.servers.models import VpnServer


def create_client(tg_id: int, days: int, limit_gb: int):
    total_bytes = limit_gb * 1024**3
    servers = list(VpnServer.objects.filter(is_active=True))
    
    try:
        user = User.objects.get(id=tg_id)
    except ObjectDoesNotExist:
        print(f"Пользователь с tg_id={tg_id} не найден.")
        return
    
    subscription = Subscription.objects.get(user=user)
    print(subscription.total_gb_limit)
    
    for server in servers:
        api = Api(
            host=server.api_url,
            username=server.api_username,
            password=server.api_password,
        )
        api.login()
        
        client = Client(
            id=subscription.vless_uuid,
            email=tg_id,
            limit_ip=1,
            total_gb=total_bytes,
            expiryTime=subscription.end_date,
            used_bytes=0,
            enable=subscription.is_vpn_client_active,
        )
        api.client.add(server.inbound_id, [client])
        print('Create client')
        
        