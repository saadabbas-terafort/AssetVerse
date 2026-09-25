from django.contrib import admin 
from django.conf import settings
from django.utils.html import format_html

from .models import (
    Orientation,
    RecordStatus,
    AssetVariant,
    FrameKey,
    FrameType,
    EffectType,
    SlideType,
    App,
    Tag,
    Category,
    Frame,
    Sticker,
    Font,
    Slide,
    Effect,
)


def image_preview(value, width=55, height=55):
    if not value:
        return "-"

    try:
        image_url = value.url
    except (AttributeError, ValueError):
        image_url = str(value)
        if not image_url.startswith(("http://", "https://", "/")):
            image_url = f"{settings.MEDIA_URL}{image_url}"

    return format_html(
        '<img src="{}" style="width:{}px;height:{}px;object-fit:cover;border-radius:6px;" />',
        image_url,
        width,
        height,
    )




class BaseLookupAdmin(admin.ModelAdmin):
    list_display = (
        "lable",
        "code",
        "is_active",
        "sortorder",
        "created_at",
        "update_at",
    )

    search_fields = (
        "lable",
        "code",
    )

    list_filter = (
        "is_active",
    )

    ordering = (
        "sortorder",
        "lable",
    )


@admin.register(Orientation)
class OrientationAdmin(BaseLookupAdmin):
    ...


@admin.register(RecordStatus)
class RecordStatusAdmin(BaseLookupAdmin):
    ...


@admin.register(AssetVariant)
class AssetVariantAdmin(BaseLookupAdmin):
    ...


@admin.register(FrameKey)
class FrameKeyAdmin(BaseLookupAdmin):
    ...


@admin.register(FrameType)
class FrameTypeAdmin(BaseLookupAdmin):
    ...


@admin.register(EffectType)
class EffectTypeAdmin(BaseLookupAdmin):
    ...


@admin.register(SlideType)
class SlideTypeAdmin(BaseLookupAdmin):
    ...




@admin.register(App)
class AppAdmin(admin.ModelAdmin):
    list_display = (
        "slug",
        "lable",
        "status",
        "sortorder",
    )

    search_fields = (
        "slug",
        "lable",
    )



@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = (
        "label",
        "tag_type",
        "code",
        "is_active",
        "create_at",
    )

    search_fields = (
        "lable",
        "code",
    )

    list_filter = (
        "tag_type",
        "is_active",
    )




@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "cover_preview",
        "title",
        "app",
        "parent",
        "status",
        "update_at",
    )

    search_fields = (
        "title",
        "app__lable",
    )

    list_filter = (
        "app",
        "status",
    )

    autocomplete_fields = (
        "app",
        "parent",
        "status",
    )

    @admin.display(description="Cover")
    def cover_preview(self, obj):
        return image_preview(obj.cover)





@admin.register(Frame)
class FrameAdmin(admin.ModelAdmin):
    list_display = (
        "cover_preview",
        "title",
        "category",
        "frame_type",
        "editor",
        "ratio_height",
    )

    search_fields = (
        "title",
        "editor",
        "category__title",
    )

    list_filter = (
        "category",
        "frame_type",
    )

    autocomplete_fields = (
        "category",
        "frame_type",
        "frame_key",
    )

    list_per_page = 50

    @admin.display(description="Cover")
    def cover_preview(self, obj):
        return image_preview(obj.cover, height=70)




@admin.register(Sticker)
class StickerAdmin(admin.ModelAdmin):
    list_display = (
        "image_preview",
        "title",
        "category",
        "status",
        "sort_order",
        "create_at",
    )

    search_fields = (
        "title",
        "category__title",
    )

    list_filter = (
        "category",
        "status",
    )

    autocomplete_fields = (
        "category",
        "status",
    )

    @admin.display(description="Image")
    def image_preview(self, obj):
        return image_preview(obj.image)




@admin.register(Font)
class FontAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "category",
        "status",
        "sort_order",
        "create_at",
        "update_at",
    )

    search_fields = (
        "title",
        "category__title",
    )

    list_filter = (
        "category",
        "status",
    )

    autocomplete_fields = (
        "category",
        "status",
    )


@admin.register(Slide)
class SlideAdmin(admin.ModelAdmin):
    list_display = (
        "cover_preview",
        "title",
        "category",
        "slide_type",
        "status",
        "sort_order",
        "create_at",
        "update_at",
    )

    search_fields = (
        "category__title",
    )

    list_filter = (
        "category",
        "slide_type",
        "status",
    )

    autocomplete_fields = (
        "category",
        "slide_type",
        "status",
    )

    @admin.display(description="Cover")
    def cover_preview(self, obj):
        return image_preview(obj.cover)




@admin.register(Effect)
class EffectAdmin(admin.ModelAdmin):
    list_display = (
        "cover_preview",
        "title",
        "category",
        "effect_type",
        "status",
        "update_at",
    )

    search_fields = (
        "title",
        "category__title",
    )

    list_filter = (
        "category",
        "effect_type",
        "status",
    )

    autocomplete_fields = (
        "category",
        "effect_type",
        "status",
    )

    @admin.display(description="Cover")
    def cover_preview(self, obj):
        return image_preview(obj.cover)