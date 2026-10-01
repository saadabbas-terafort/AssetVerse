from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import PublicUser, PublicUserToken, User


@admin.register(User)
class StaffUserAdmin(UserAdmin):
    ordering = ("email",)
    list_display = ("email", "first_name", "last_name", "is_staff", "is_active")
    search_fields = ("email", "first_name", "last_name")
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = ((None, {"classes": ("wide",), "fields": ("email", "password1", "password2")}),)


@admin.register(PublicUser)
class PublicUserAdmin(admin.ModelAdmin):
    list_display = ("device_id", "app_name", "is_active", "created_at")
    search_fields = ("device_id", "app_name")
    list_filter = ("app_name", "is_active")


@admin.register(PublicUserToken)
class PublicUserTokenAdmin(admin.ModelAdmin):
    list_display = ("key", "user", "created")
    search_fields = ("key", "user__device_id", "user__app_name")