import uuid

from django.db import models

from apps.utils.asset_paths import sticker_upload_path
from apps.utils.validation import validate_asset_category


class Sticker(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    category = models.ForeignKey("category.Category", on_delete=models.CASCADE, related_name="stickers")
    image = models.ImageField(max_length=500, upload_to=sticker_upload_path)
    status = models.ForeignKey("lookup.RecordStatus", on_delete=models.PROTECT, related_name="stickers")
    tags = models.ManyToManyField(
        "lookup.Tag",
        blank=True,
        related_name="stickers",
        through="StickerTag",
        through_fields=("sticker", "tag"),
    )
    sort_order = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "stickers_sticker"
        ordering = ("sort_order", "title")
        indexes = [
            models.Index(fields=("category", "status", "sort_order"), name="sticker_cat_status_sort_idx"),
        ]

    def clean(self):
        validate_asset_category(self, "sticker")

    def __str__(self):
        return self.title


class StickerTag(models.Model):
    pk = models.CompositePrimaryKey("sticker_id", "tag_id")
    sticker = models.ForeignKey(Sticker, on_delete=models.CASCADE, related_name="+")
    tag = models.ForeignKey("lookup.Tag", on_delete=models.CASCADE, related_name="+")

    class Meta:
        db_table = "stickers_sticker_tags"