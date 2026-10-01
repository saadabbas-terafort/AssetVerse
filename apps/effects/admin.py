from django.contrib import admin

from apps.home_assets.admin import image_preview
from .models import Effect


@admin.register(Effect)
class EffectAdmin(admin.ModelAdmin):
    list_display = ("cover_preview", "title", "category", "effect_type", "status", "sort_order")
    search_fields = ("title", "category__title")
    list_filter = ("category", "effect_type", "status")
    autocomplete_fields = ("category", "effect_type", "status", "tags")

    @admin.display(description="Cover")
    def cover_preview(self, obj):
        return image_preview(obj.cover)