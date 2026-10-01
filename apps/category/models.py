import uuid

from django.core.exceptions import ValidationError
from django.db import models

from apps.lookup.models import Tag
from apps.utils.asset_paths import category_cover_upload_path


class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    app = models.ForeignKey(
        "app_settings.AppSetting",
        on_delete=models.PROTECT,
        related_name="categories",
    )
    title = models.CharField(max_length=255)
    actionbar = models.CharField(max_length=255, blank=True, default="")
    cover_image = models.ImageField(max_length=500, upload_to=category_cover_upload_path)
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="children",
    )
    orientation = models.ForeignKey(
        "lookup.Orientation",
        on_delete=models.PROTECT,
        related_name="categories",
    )
    tag = models.ForeignKey(
        "lookup.Tag",
        on_delete=models.PROTECT,
        related_name="categories",
    )
    section = models.ForeignKey(
        "lookup.Tag",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="sections",
    )
    status = models.ForeignKey(
        "lookup.RecordStatus",
        on_delete=models.PROTECT,
        related_name="categories",
    )
    variant = models.ForeignKey(
        "lookup.AssetVariant",
        on_delete=models.PROTECT,
        related_name="categories",
    )
    api_option = models.CharField(max_length=100, blank=True, default="")
    sort_order = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "category_homecategory"
        ordering = ("sort_order", "title")
        indexes = [
            models.Index(fields=("app", "section", "status", "sort_order"), name="homecat_app_section_status_idx"),
            models.Index(fields=("app", "parent"), name="homecat_app_parent_idx"),
            models.Index(fields=("app", "variant", "status"), name="homecat_app_variant_status_idx"),
        ]

    def clean(self):
        errors = {}
        if self.parent_id:
            if self.parent_id == self.pk:
                errors["parent"] = "A category cannot be its own parent."
            elif self.parent.parent_id:
                errors["parent"] = "Categories may have only a parent and one child level."
            elif self.parent.app_id != self.app_id:
                errors["parent"] = "A child and its parent must belong to the same app."
        if self.tag_id and self.tag.tag_type != Tag.TagType.AVAILABILITY:
            errors["tag"] = "Category tag must have the availability type."
        if self.section_id and self.section.tag_type != Tag.TagType.LISTING:
            errors["section"] = "Category section must have the listing type."
        if errors:
            raise ValidationError(errors)

    def __str__(self):
        return self.title