import uuid

from django.db import models


class Tariff(models.Model):
    name = models.CharField(
        max_length=100, verbose_name="Название тарифа (для админки)"
    )
    duration_days = models.PositiveIntegerField(verbose_name="Длительность (дни)")
    price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Цена (руб)"
    )
    is_active = models.BooleanField(default=True, verbose_name="Активен")
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок сортировки")
    is_bestseller = models.BooleanField(default=False, verbose_name="Бестселлер")
    original_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Старая цена (зачеркнутая)",
    )

    def __str__(self):
        return f"{self.name} ({self.duration_days} дней за {self.price} руб)"

    class Meta:
        verbose_name = "Тариф"
        verbose_name_plural = "Тарифы"
        ordering = ["order"]
        
        
class Payment(models.Model):
    STATUS = (
        ('pending', 'Ожидание'),
        ('canseled', 'Отменен'),
        ('successful', 'Успешный')
    )
    payment_id = models.CharField(
        max_length=36,  
        unique=True,    
        verbose_name="ID платежа в ЮKassa"
    )
    user = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name="payments",
        verbose_name="Пользователь",
    )
    
    tariff = models.ForeignKey(
        Tariff,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Тариф",
    )
    
    status = models.CharField(choices=STATUS, default='pending', verbose_name='Статус платежа')
    create_at = models.DateTimeField(auto_created=True, verbose_name='Дата создания платежа')
    
    def __str__(self):
        return f"Пользователь {self.user.id} | Тариф {self.tariff.name}"
    
    
    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"
