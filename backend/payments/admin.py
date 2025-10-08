from django.contrib import admin

from .models import Tariff


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