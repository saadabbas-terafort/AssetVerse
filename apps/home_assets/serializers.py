from django.db import transaction
from rest_framework import serializers

from apps.home_assets.models import Frame, FrameAsset, FrameConstraint
from apps.lookup.models import FrameKey, FrameType, RecordStatus, Tag
from apps.utils.serializer_fields import ActiveCodeRelatedField
from apps.utils.serializers import AssetValidationMixin


class FrameConstraintSerializer(serializers.ModelSerializer):
    class Meta:
        model = FrameConstraint
        fields = ("id", "value_1", "value_2", "value_3", "value_4", "sort_order", "created_at", "updated_at")
        read_only_fields = ("id", "created_at", "updated_at")


class FrameAssetSerializer(serializers.ModelSerializer):
    frame = serializers.PrimaryKeyRelatedField(queryset=Frame.objects.all())
    key = ActiveCodeRelatedField(queryset=FrameKey.objects.all())
    status = ActiveCodeRelatedField(queryset=RecordStatus.objects.all())

    class Meta:
        model = FrameAsset
        fields = ("id", "frame", "key", "image", "status", "sort_order", "created_at", "updated_at")
        read_only_fields = ("id", "created_at", "updated_at")


class FrameReadAssetSerializer(serializers.ModelSerializer):
    key = ActiveCodeRelatedField(read_only=True)
    status = ActiveCodeRelatedField(read_only=True)

    class Meta:
        model = FrameAsset
        fields = ("key", "image", "status", "sort_order")


class FrameSerializer(AssetValidationMixin, serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Frame._meta.get_field("category").remote_field.model.objects.all())
    frame_type = ActiveCodeRelatedField(queryset=FrameType.objects.all())
    status = ActiveCodeRelatedField(queryset=RecordStatus.objects.all())
    tags = ActiveCodeRelatedField(queryset=Tag.objects.all(), many=True, required=False)
    constraints = FrameConstraintSerializer(many=True, required=False)
    assets = FrameReadAssetSerializer(many=True, read_only=True)

    class Meta:
        model = Frame
        fields = (
            "id", "title", "category", "frame_type", "editor", "ratio_width", "ratio_height",
            "status", "image_picker", "tags", "sort_order", "constraints", "assets", "created_at", "updated_at",
        )
        read_only_fields = ("id", "assets", "created_at", "updated_at")

    @transaction.atomic
    def create(self, validated_data):
        constraints = validated_data.pop("constraints", [])
        tags = validated_data.pop("tags", [])
        frame = super().create(validated_data)
        frame.tags.set(tags)
        FrameConstraint.objects.bulk_create(
            [FrameConstraint(frame=frame, **constraint) for constraint in constraints]
        )
        return frame

    @transaction.atomic
    def update(self, instance, validated_data):
        constraints_present = "constraints" in validated_data
        constraints = validated_data.pop("constraints", None)
        tags_present = "tags" in validated_data
        tags = validated_data.pop("tags", None)
        frame = super().update(instance, validated_data)
        if tags_present:
            frame.tags.set(tags)
        if constraints_present:
            frame.constraints.all().delete()
            FrameConstraint.objects.bulk_create(
                [FrameConstraint(frame=frame, **constraint) for constraint in constraints]
            )
        return frame