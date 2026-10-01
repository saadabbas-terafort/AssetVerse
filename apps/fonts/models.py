import uuid

from django.core.validators import FileExtensionValidator
from django.db import models

from apps.utils.asset_paths import font_upload_path
from apps.utils.validation import validate_asset_category


class Font(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    category = models.ForeignKey("category.Category", on_delete=models.CASCADE, related_name="fonts")
    file = models.FileField(
        upload_to=font_upload_path,
        max_length=500,
        validators=(FileExtensionValidator(allowed_extensions=("ttf",)),),
    )
    status = models.ForeignKey("lookup.RecordStatus", on_delete=models.PROTECT, related_name="fonts")
    tags = models.ManyToManyField("lookup.Tag", blank=True, related_name="fonts", db_table="fonts_font_tags")
    sort_order = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "fonts_font"
        ordering = ("sort_order", "title")
        indexes = [
            models.Index(fields=("category", "status", "sort_order"), name="font_cat_status_sort_idx"),
        ]

    def clean(self):
        validate_asset_category(self, "font")

    def __str__(self):
        return self.title