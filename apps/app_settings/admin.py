from django.contrib import admin

from .models import AppSetting


@admin.register(AppSetting)
class AppSettingAdmin(admin.ModelAdmin):
    list_display = ("slug", "label", "is_active", "sort_order")
    search_fields = ("slug", "label")
    list_filter = ("is_active",)
    ordering = ("sort_order", "label")