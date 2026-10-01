import uuid

from django.db import models

from apps.utils.asset_paths import frame_asset_upload_path
from apps.utils.validation import validate_asset_category


class Frame(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    category = models.ForeignKey("category.Category", on_delete=models.CASCADE, related_name="frames")
    frame_type = models.ForeignKey("lookup.FrameType", on_delete=models.PROTECT, related_name="frames")
    editor = models.CharField(max_length=255, default="frames")
    ratio_width = models.DecimalField(max_digits=8, decimal_places=2)
    ratio_height = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.ForeignKey("lookup.RecordStatus", on_delete=models.PROTECT, related_name="frames")
    image_picker = models.BooleanField(default=True)
    sort_order = models.IntegerField()
    tags = models.ManyToManyField("lookup.Tag", blank=True, related_name="frames", db_table="home_assets_frame_tags")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "home_assets_frame"
        ordering = ("sort_order", "title")
        indexes = [
            models.Index(fields=("category", "status", "sort_order"), name="frame_cat_status_sort_idx"),
        ]

    def clean(self):
        validate_asset_category(self, "frame")

    def __str__(self):
        return self.title


class FrameConstraint(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    frame = models.ForeignKey(Frame, on_delete=models.CASCADE, related_name="constraints")
    value_1 = models.DecimalField(max_digits=8, decimal_places=4)
    value_2 = models.DecimalField(max_digits=8, decimal_places=4)
    value_3 = models.DecimalField(max_digits=8, decimal_places=4)
    value_4 = models.DecimalField(max_digits=8, decimal_places=4)
    sort_order = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "home_assets_frameconstraint"
        ordering = ("sort_order", "created_at")


class FrameAsset(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    frame = models.ForeignKey(Frame, on_delete=models.CASCADE, related_name="assets")
    key = models.ForeignKey("lookup.FrameKey", on_delete=models.PROTECT, related_name="frame_assets")
    image = models.ImageField(max_length=500, upload_to=frame_asset_upload_path)
    status = models.ForeignKey("lookup.RecordStatus", on_delete=models.PROTECT, related_name="frame_assets")
    sort_order = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "home_assets_frameasset"
        ordering = ("sort_order", "created_at")
        indexes = [
            models.Index(fields=("frame", "status", "sort_order"), name="frameasset_frame_status_idx"),
        ]