from django.contrib import admin

from .models import Tariff, Payment


@admin.register(Tariff)
class TariffAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "duration_days",
        "price",
        "is_active",
        "order",
        "is_bestseller",
    )
    list_editable = ("is_active", "order", "price", "is_bestseller")
    list_filter = ("is_active",)
    
    
@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        "payment_id",
        "user",
        "tariff",
        "status",
        "create_at",
    )
    search_fields = ("user", "tariff", "status", "create_at", "payment_id")
    readonly_fields = ("payment_id",)