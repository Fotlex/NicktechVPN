from py3xui import Api, Client

from datetime import timedelta, datetime

from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist

from backend.users.models import User, Subscription
from backend.servers.models import VpnServer


def create_client(tg_id: int, limit_gb: int):
    total_bytes = limit_gb * 1024**3
    servers = list(VpnServer.objects.filter(is_active=True))
    
    try:
        user = User.objects.get(id=tg_id)
        subscription = Subscription.objects.get(user=user)
    except ObjectDoesNotExist:
        print(f"Пользователь с tg_id={tg_id} не найден.")
        return
    
    expiry_time = int(subscription.end_date.timestamp() * 1000)
    
    for server in servers:
        api = Api(
            host=server.api_url,
            username=server.api_username,
            password=server.api_password,
        )
        api.login()
        
        client = Client(
            id=str(subscription.vless_uuid),
            email=str(tg_id),
            limit_ip=1,
            total_gb=total_bytes,
            expiryTime=expiry_time,
            used_bytes=0,
            enable=subscription.is_vpn_client_active,
        )
        api.client.add(server.inbound_id, [client])
        print('Create client')
      
      
def auto_update_data(subscription: Subscription, subscription_end: int, limit_gb: int, used_traffic: int):
    date_end_time = datetime.fromtimestamp(subscription_end / 1000, tz=timezone.get_current_timezone())
    
    subscription.end_date = date_end_time
    subscription.used_bytes = used_traffic
    subscription.is_vpn_client_active = date_end_time > timezone.now()
    subscription.total_bytes_limit = limit_gb / 1024**3
    
    subscription.save()
        
        
def update_client(tg_id: int, days: int, gb_limit: int):
    servers = list(VpnServer.objects.filter(is_active=True))
    
    try:
        user = User.objects.get(id=tg_id)
        subscription = Subscription.objects.get(user=user)
    except ObjectDoesNotExist:
        print(f"Пользователь с tg_id={tg_id} не найден.")
        return
    
    for server in servers:   
        api = Api(
            host=server.api_url,
            username=server.api_username,
            password=server.api_password,
        )
        api.login()
        
        client = api.client.get_by_email(email=str(tg_id))
        if client.expiry_time > int(timezone.now().timestamp() * 1000):
            client.expiry_time += days * 24 * 60 * 60 * 1000
            total_gb = client.total_gb
            client.total_gb = total_gb + gb_limit * 1024**3
        else:
            client.expiry_time = int((timezone.now() + timedelta(days=days)).timestamp() * 1000)
            
            client.up = 0
            client.down = 0
            client.enable = True
            client.total_gb = gb_limit * 1024**3
            
        client.id = str(subscription.vless_uuid)
        api.client.update(str(subscription.vless_uuid), client)
        
        auto_update_data(
            subscription=subscription,
            subscription_end=client.expiry_time,
            limit_gb=client.total_gb,
            used_traffic=client.up + client.down,
        )
        
        
def add_client_to_server(user: User, server: VpnServer):
    try:
        subscription = Subscription.objects.get(user=user)
    except Exception:
        pass
    
    api = Api(
            host=server.api_url,
            username=server.api_username,
            password=server.api_password,
        )
    api.login()
    
    client = Client(
        id=str(subscription.vless_uuid),
        email=str(user.id),
        limit_ip=1,
        total_gb=subscription.total_bytes_limit,
        expiryTime=int(subscription.end_date.timestamp() * 1000),
        used_bytes=subscription.used_bytes,
        enable=subscription.is_vpn_client_active,
    )
    api.client.add(server.inbound_id, [client])
        