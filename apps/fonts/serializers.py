from rest_framework import serializers

from apps.lookup.models import RecordStatus, Tag
from apps.utils.serializer_fields import ActiveCodeRelatedField
from apps.utils.serializers import AssetValidationMixin

from .models import Font


class FontSerializer(AssetValidationMixin, serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Font._meta.get_field("category").remote_field.model.objects.all())
    status = ActiveCodeRelatedField(queryset=RecordStatus.objects.all())
    tags = ActiveCodeRelatedField(queryset=Tag.objects.all(), many=True, required=False)

    class Meta:
        model = Font
        fields = ("id", "title", "category", "file", "status", "tags", "sort_order", "created_at", "updated_at")
        read_only_fields = ("id", "created_at", "updated_at")