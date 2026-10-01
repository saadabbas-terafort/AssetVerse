import uuid

from django.db import models

from apps.utils.asset_paths import tag_icon_upload_path


class BaseLookup(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.SlugField(max_length=50, unique=True)
    label = models.CharField(max_length=100)
    sort_order = models.SmallIntegerField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ("sort_order", "label")

    def __str__(self):
        return self.label


class Orientation(BaseLookup):
    class Meta(BaseLookup.Meta):
        abstract = False
        db_table = "lookup_orientation"


class RecordStatus(BaseLookup):
    class Meta(BaseLookup.Meta):
        abstract = False
        db_table = "lookup_recordstatus"


class AssetVariant(BaseLookup):
    class Meta(BaseLookup.Meta):
        abstract = False
        db_table = "lookup_assetvariant"


class FrameKey(BaseLookup):
    class Meta(BaseLookup.Meta):
        abstract = False
        db_table = "lookup_framekey"


class FrameType(BaseLookup):
    class Meta(BaseLookup.Meta):
        abstract = False
        db_table = "lookup_frametype"


class EffectType(BaseLookup):
    class Meta(BaseLookup.Meta):
        abstract = False
        db_table = "lookup_effecttype"


class SlideType(BaseLookup):
    class Meta(BaseLookup.Meta):
        abstract = False
        db_table = "lookup_slidetype"


class Tag(BaseLookup):
    class TagType(models.TextChoices):
        SCREEN = "screen", "Screen"
        LISTING = "listing", "Listing"
        AVAILABILITY = "availability", "Availability"
        VARIANT = "variant", "Variant"
        HASHTAG = "hashtag", "Hashtag"
        LOCALE = "locale", "Locale"

    tag_type = models.CharField(max_length=20, choices=TagType.choices)
    icon = models.ImageField(
        upload_to=tag_icon_upload_path,
        max_length=500,
        null=True,
        blank=True,
    )

    class Meta(BaseLookup.Meta):
        abstract = False
        db_table = "lookup_tag"
        indexes = [
            models.Index(
                fields=("tag_type", "is_active", "sort_order"),
                name="tag_type_active_sort_idx",
            ),
        ]