from rest_framework import serializers

from .models import AssetVariant, EffectType, FrameKey, FrameType, Orientation, RecordStatus, SlideType, Tag


class LookupSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"


class OrientationSerializer(LookupSerializer):
    class Meta(LookupSerializer.Meta):
        model = Orientation


class RecordStatusSerializer(LookupSerializer):
    class Meta(LookupSerializer.Meta):
        model = RecordStatus


class AssetVariantSerializer(LookupSerializer):
    class Meta(LookupSerializer.Meta):
        model = AssetVariant


class FrameKeySerializer(LookupSerializer):
    class Meta(LookupSerializer.Meta):
        model = FrameKey


class FrameTypeSerializer(LookupSerializer):
    class Meta(LookupSerializer.Meta):
        model = FrameType


class EffectTypeSerializer(LookupSerializer):
    class Meta(LookupSerializer.Meta):
        model = EffectType


class SlideTypeSerializer(LookupSerializer):
    class Meta(LookupSerializer.Meta):
        model = SlideType


class TagSerializer(LookupSerializer):
    class Meta(LookupSerializer.Meta):
        model = Tag