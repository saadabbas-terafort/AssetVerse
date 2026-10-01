import uuid

from django.db import models

from apps.utils.asset_paths import slide_cover_upload_path
from apps.utils.validation import validate_asset_category


class Slide(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    category = models.ForeignKey("category.Category", on_delete=models.CASCADE, related_name="slides")
    slide_type = models.ForeignKey("lookup.SlideType", on_delete=models.PROTECT, related_name="slides")
    cover = models.ImageField(max_length=500, upload_to=slide_cover_upload_path)
    status = models.ForeignKey("lookup.RecordStatus", on_delete=models.PROTECT, related_name="slides")
    sort_order = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "slides_slide"
        ordering = ("sort_order", "title")
        indexes = [
            models.Index(fields=("category", "status", "sort_order"), name="slide_cat_status_sort_idx"),
            models.Index(fields=("slide_type", "status", "sort_order"), name="slide_type_status_sort_idx"),
        ]

    def clean(self):
        validate_asset_category(self, "slide")

    def __str__(self):
        return self.title