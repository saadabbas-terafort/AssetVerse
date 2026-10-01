from django.contrib import admin
from django.conf import settings
from django.utils.html import format_html

from .models import Frame, FrameAsset, FrameConstraint


def image_preview(value, width=55, height=55):
    if not value:
        return "-"
    try:
        image_url = value.url
    except (AttributeError, ValueError):
        image_url = str(value)
        if not image_url.startswith(("http://", "https://", "/")):
            image_url = f"{settings.MEDIA_URL}{image_url}"
    return format_html('<img src="{}" style="width:{}px;height:{}px;object-fit:cover;border-radius:6px;" />', image_url, width, height)


class FrameConstraintInline(admin.TabularInline):
    model = FrameConstraint
    extra = 0


class FrameAssetInline(admin.TabularInline):
    model = FrameAsset
    extra = 0


@admin.register(Frame)
class FrameAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "frame_type", "status", "sort_order")
    search_fields = ("title", "editor", "category__title")
    list_filter = ("category", "frame_type", "status")
    autocomplete_fields = ("category", "frame_type", "status", "tags")
    inlines = (FrameConstraintInline, FrameAssetInline)
    list_per_page = 50


@admin.register(FrameAsset)
class FrameAssetAdmin(admin.ModelAdmin):
    list_display = ("image_preview", "frame", "key", "status", "sort_order")
    list_filter = ("key", "status")
    autocomplete_fields = ("frame", "key", "status")

    @admin.display(description="Image")
    def image_preview(self, obj):
        return image_preview(obj.image)


@admin.register(FrameConstraint)
class FrameConstraintAdmin(admin.ModelAdmin):
    list_display = ("frame", "sort_order", "created_at")
    autocomplete_fields = ("frame",)