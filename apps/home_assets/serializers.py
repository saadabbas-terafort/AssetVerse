from rest_framework import serializers

from .models import Frame, FrameAsset, FrameConstraint


class FrameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Frame
        fields = "__all__"


class FrameAssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = FrameAsset
        fields = "__all__"


class FrameConstraintSerializer(serializers.ModelSerializer):
    class Meta:
        model = FrameConstraint
        fields = "__all__"