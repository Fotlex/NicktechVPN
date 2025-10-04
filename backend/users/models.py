import uuid

from datetime import timedelta

from django.utils import timezone
from django.db import models


class User(models.Model):
    id = models.BigIntegerField(
        unique=True, primary_key=True, verbose_name="Телеграм ID"
    )
    username = models.CharField(
        max_length=255, null=True, blank=True, verbose_name="Юзернейм"
    )
    first_name = models.CharField(
        max_length=255, null=True, blank=True, verbose_name="Имя"
    )

    referred_by = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="referrals",
        verbose_name="Кто пригласил",
    )
    date_joined = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата регистрации"
    )

    def __str__(self):
        return f"id: {self.id}"

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        
        
class Subscription(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="subscription",
        verbose_name="Пользователь",
    )
    end_date = models.DateTimeField(verbose_name="Дата окончания")
    vless_uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    trial_activated = models.BooleanField(
        default=False, verbose_name="Триал активирован"
    )

    total_paid = models.DecimalField(
        max_digits=10, decimal_places=2, default=0, verbose_name="Всего пополнено"
    )

    is_vpn_client_active = models.BooleanField(
        default=False, verbose_name="Клиент VPN активен в 3x-ui"
    )

    total_bytes_limit = models.BigIntegerField(
        default=268435456000, verbose_name="Лимит трафика (байты)"
    )
    used_bytes = models.BigIntegerField(
        default=0, verbose_name="Использовано трафика (байты)"
    )
    last_traffic_update = models.DateTimeField(
        null=True, blank=True, verbose_name="Последнее обновление трафика"
    )

    @property
    def is_active(self):
        return self.end_date > timezone.now()

    @property
    def used_gb(self):
        return round(self.used_bytes / (1024**3), 2)

    @property
    def total_gb_limit(self):
        return round(self.total_bytes_limit / (1024**3), 2)

    def extend_subscription(self, days: int):
        if self.end_date < timezone.now():
            self.end_date = timezone.now()
        self.end_date += timedelta(days=days)
        self.save()

    def __str__(self):
        return f"Подписка для {self.user}"

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"
