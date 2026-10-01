from django.contrib import admin

from apps.home_assets.admin import image_preview
from .models import Slide


@admin.register(Slide)
class SlideAdmin(admin.ModelAdmin):
    list_display = ("cover_preview", "title", "category", "slide_type", "status", "sort_order")
    search_fields = ("title", "category__title")
    list_filter = ("category", "slide_type", "status")
    autocomplete_fields = ("category", "slide_type", "status")

    @admin.display(description="Cover")
    def cover_preview(self, obj):
        return image_preview(obj.cover)