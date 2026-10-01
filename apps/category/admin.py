from django.contrib import admin
from django.conf import settings
from django.utils.html import format_html

from .models import Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("cover_preview", "title", "app", "parent", "status", "updated_at")
    search_fields = ("title", "app__label")
    list_filter = ("app", "status", "variant")
    autocomplete_fields = ("app", "parent", "orientation", "tag", "section", "status", "variant")

    @admin.display(description="Cover")
    def cover_preview(self, obj):
        try:
            image_url = obj.cover_image.url
        except (AttributeError, ValueError):
            image_url = f"{settings.MEDIA_URL}{obj.cover_image}"
        return format_html('<img src="{}" style="width:55px;height:55px;object-fit:cover;border-radius:6px;" />', image_url)