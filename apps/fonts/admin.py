from django.contrib import admin

from .models import Font


@admin.register(Font)
class FontAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "status", "sort_order", "created_at", "updated_at")
    search_fields = ("title", "category__title")
    list_filter = ("category", "status")
    autocomplete_fields = ("category", "status", "tags")