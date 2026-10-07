from rest_framework import serializers

from apps.lookup.models import RecordStatus, SlideType
from apps.utils.serializer_fields import ActiveCodeRelatedField
from apps.utils.serializers import AssetValidationMixin

from .models import Slide


class SlideSerializer(AssetValidationMixin, serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Slide._meta.get_field("category").remote_field.model.objects.all())
    slide_type = ActiveCodeRelatedField(queryset=SlideType.objects.all())
    status = ActiveCodeRelatedField(queryset=RecordStatus.objects.all())

    class Meta:
        model = Slide
        fields = ("id", "title", "category", "slide_type", "cover", "status", "sort_order", "created_at", "updated_at")
        read_only_fields = ("id", "created_at", "updated_at")