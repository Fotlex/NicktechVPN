from django.apps import AppConfig


class ServersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'backend.servers'
    verbose_name = 'VPN Сервера'
    
    def ready(self):
        import backend.servers.signals
