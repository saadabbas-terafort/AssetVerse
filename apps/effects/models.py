import uuid

from django.db import models

from apps.utils.asset_paths import effect_cover_upload_path, effect_file_upload_path
from apps.utils.validation import validate_asset_category


class Effect(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    effect = models.CharField(max_length=100)
    category = models.ForeignKey("category.Category", on_delete=models.CASCADE, related_name="effects")
    effect_type = models.ForeignKey("lookup.EffectType", on_delete=models.PROTECT, related_name="effects")
    cover = models.ImageField(max_length=500, upload_to=effect_cover_upload_path)
    file = models.FileField(max_length=500, upload_to=effect_file_upload_path)
    status = models.ForeignKey("lookup.RecordStatus", on_delete=models.PROTECT, related_name="effects")
    tags = models.ManyToManyField(
        "lookup.Tag",
        blank=True,
        related_name="effects",
        through="EffectTag",
        through_fields=("effect", "tag"),
    )
    sort_order = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "effects_effect"
        ordering = ("sort_order", "title")
        indexes = [
            models.Index(fields=("category", "status", "sort_order"), name="effect_cat_status_sort_idx"),
            models.Index(fields=("effect_type", "status"), name="effect_type_status_idx"),
        ]

    def clean(self):
        validate_asset_category(self, "effect")

    def __str__(self):
        return self.title


class EffectTag(models.Model):
    pk = models.CompositePrimaryKey("effect_id", "tag_id")
    effect = models.ForeignKey(Effect, on_delete=models.CASCADE, related_name="+")
    tag = models.ForeignKey("lookup.Tag", on_delete=models.CASCADE, related_name="+")

    class Meta:
        db_table = "effects_effect_tags"