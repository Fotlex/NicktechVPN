from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "username",
        "first_name",
        "referred_by",
        "date_joined",
    )
    search_fields = ("id", "username", "first_name")
    list_filter = ("date_joined",)
    raw_id_fields = ("referred_by",)

    def has_add_permission(self, request):
        return False