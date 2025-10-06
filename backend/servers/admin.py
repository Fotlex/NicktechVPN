from django.contrib import admin

from .models import VpnServer


@admin.register(VpnServer)
class VpnServerAdmin(admin.ModelAdmin):
    list_display = ("name", "api_url", "inbound_id", "is_active")
    list_editable = ("is_active",)
    list_filter = ("is_active",)
