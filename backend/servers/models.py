from django.db import models

class VpnServer(models.Model):
    name = models.CharField(
        max_length=100, verbose_name="Название сервера (для админки)"
    )
    api_url = models.URLField(
        verbose_name="URL API 3x-ui", help_text="Пример: http://your_server_ip:2053"
    )
    api_username = models.CharField(max_length=100, verbose_name="Логин API")
    api_password = models.CharField(max_length=100, verbose_name="Пароль API")
    api_token = models.CharField(verbose_name="Токен API", blank=True, null=True)
    inbound_id = models.PositiveIntegerField(
        default=1, verbose_name="ID входящего подключения"
    )
    
    domen = models.CharField(verbose_name='Домен и порт', max_length=100, null=True, blank=True)
    public_key = models.CharField(null=True, blank=True, verbose_name='Публичный ключ', max_length=255)
    website_name = models.CharField(null=True, blank=True, verbose_name='Имя вебсайта', max_length=255)
    short_id = models.CharField(null=True, blank=True, verbose_name='Короткий ID', max_length=255)
    
    is_active = models.BooleanField(default=True, verbose_name="Сервер активен")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "VPN Сервер"
        verbose_name_plural = "VPN Серверы"
