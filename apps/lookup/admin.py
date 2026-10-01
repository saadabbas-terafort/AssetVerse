from django.contrib import admin

from .models import AssetVariant, EffectType, FrameKey, FrameType, Orientation, RecordStatus, SlideType, Tag


class BaseLookupAdmin(admin.ModelAdmin):
    list_display = ("label", "code", "is_active", "sort_order", "created_at", "updated_at")
    search_fields = ("label", "code")
    list_filter = ("is_active",)
    ordering = ("sort_order", "label")


for model in (Orientation, RecordStatus, AssetVariant, FrameKey, FrameType, EffectType, SlideType):
    admin.site.register(model, BaseLookupAdmin)


@admin.register(Tag)
class TagAdmin(BaseLookupAdmin):
    list_display = BaseLookupAdmin.list_display + ("tag_type",)
    list_filter = ("tag_type", "is_active")