from rest_framework import serializers

from apps.lookup.models import EffectType, RecordStatus, Tag
from apps.utils.serializer_fields import ActiveCodeRelatedField
from apps.utils.serializers import AssetValidationMixin

from .models import Effect


class EffectSerializer(AssetValidationMixin, serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Effect._meta.get_field("category").remote_field.model.objects.all())
    effect_type = ActiveCodeRelatedField(queryset=EffectType.objects.all())
    status = ActiveCodeRelatedField(queryset=RecordStatus.objects.all())
    tags = ActiveCodeRelatedField(queryset=Tag.objects.all(), many=True, required=False)

    class Meta:
        model = Effect
        fields = (
            "id", "title", "effect", "category", "effect_type", "cover", "file",
            "status", "tags", "sort_order", "created_at", "updated_at",
        )
        read_only_fields = ("id", "created_at", "updated_at")