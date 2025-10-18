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
      
      
def auto_update_data(subscription: Subscription):
    servers = list(VpnServer.objects.filter(is_active=True))
    
    trafic_sum = 0
    
    for server in servers:   
        api = Api(
            host=server.api_url,
            username=server.api_username,
            password=server.api_password,
        )
        api.login()
        user = subscription.user
        client = api.client.get_by_email(email=str(user.id))
        trafic_sum += client.down + client.up
        client.id = str(subscription.vless_uuid)
        
    subscription.used_bytes = trafic_sum
    
    if trafic_sum > subscription.total_bytes_limit:
        subscription.is_vpn_client_active = False
        
        for server in servers:
            api = Api(
                host=server.api_url,
                username=server.api_username,
                password=server.api_password,
            )
            api.login()
            user = subscription.user
            client = api.client.get_by_email(email=str(user.id))
            client.enable = False
            client.id = str(subscription.vless_uuid)
            api.client.update(str(subscription.vless_uuid), client)
    
    if subscription.end_date < timezone.now():
        subscription.is_vpn_client_active = False
    
    subscription.last_traffic_update = timezone.now()
    subscription.save()
        
        
def update_client(tg_id: int, days: int, gb_limit: int):
    servers = list(VpnServer.objects.filter(is_active=True))
    
    try:
        user = User.objects.get(id=tg_id)
        subscription = Subscription.objects.get(user=user)
        
        subscription.last_traffic_update = timezone.now()
        
        if subscription.end_date < timezone.now():
            subscription.end_date = timezone.now() + timedelta(days=days)
            subscription.total_bytes_limit = gb_limit * 1024**3
            subscription.used_bytes = 0
        else:
            subscription.end_date += timedelta(days=days)
            subscription.total_bytes_limit += gb_limit * 1024**3
        
        subscription.is_vpn_client_active = True
        subscription.save()
    except ObjectDoesNotExist:
        print(f"Пользователь с tg_id={tg_id} не найден.")
        return
    
    try:
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
                client.total_gb = subscription.total_bytes_limit
            else:
                client.expiry_time = int((timezone.now() + timedelta(days=days)).timestamp() * 1000)
                
                client.up = 0
                client.down = 0
                
                client.total_gb = subscription.total_bytes_limit
            
            client.enable = True
            client.id = str(subscription.vless_uuid)
            api.client.update(str(subscription.vless_uuid), client)

    except Exception as e:
        print(e)

        
        
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
   
   
def get_connection_string(user_uuid, server: VpnServer):
    connection_string = (
        f"vless://{user_uuid}@{server.domen}"
        f"?type=tcp&security=reality&pbk={server.public_key}&fp=firefox&sni={server.website_name}"
        f"&sid={server.short_id}&spx=%2F#{server.name}"
    )

    return connection_string
        
        
def get_combined_subscriptions(subscription: Subscription):
    servers = VpnServer.objects.filter(is_active=True)

    combined_subscriptions = [
        get_connection_string(subscription.vless_uuid, server) for server in servers
    ]

    return combined_subscriptions
