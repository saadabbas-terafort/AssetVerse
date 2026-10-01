from django.contrib import admin

from apps.home_assets.admin import image_preview
from .models import Sticker


@admin.register(Sticker)
class StickerAdmin(admin.ModelAdmin):
    list_display = ("image_preview", "title", "category", "status", "sort_order", "created_at")
    search_fields = ("title", "category__title")
    list_filter = ("category", "status")
    autocomplete_fields = ("category", "status", "tags")

    @admin.display(description="Image")
    def image_preview(self, obj):
        return image_preview(obj.image)