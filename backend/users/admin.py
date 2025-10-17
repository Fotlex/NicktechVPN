from django.contrib import admin

from .models import User, Subscription


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "username",
        "first_name",
        "referred_by",
        "date_joined",
        "refferal_balance",
        'total_paid',
    )
    search_fields = ("id", "username", "first_name")
    list_filter = ("date_joined",)
    raw_id_fields = ("referred_by",)

    def has_add_permission(self, request):
        return False
    

@admin.register(Subscription) 
class Subscription(admin.ModelAdmin):
    list_display = (
        'user',
        'end_date',
        'vless_uuid',
        'is_vpn_client_active',
        'total_bytes_limit',
        'used_bytes',
    )
    readonly_fields = (
        'vless_uuid',
    )
    