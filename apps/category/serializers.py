from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers

from apps.app_settings.models import AppSetting
from apps.lookup.models import AssetVariant, Orientation, RecordStatus, Tag
from apps.utils.serializer_fields import AppSlugField, NestedCodeRelatedField

from .models import Category


class CategorySerializer(serializers.ModelSerializer):
    app = AppSlugField(queryset=AppSetting.objects.all())
    app_name = serializers.CharField(source="app.slug", read_only=True)
    parent = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), allow_null=True, required=False)
    orientation = NestedCodeRelatedField(queryset=Orientation.objects.all())
    tag = NestedCodeRelatedField(queryset=Tag.objects.all())
    section = NestedCodeRelatedField(queryset=Tag.objects.all(), allow_null=True, required=False)
    status = NestedCodeRelatedField(queryset=RecordStatus.objects.all())
    variant = NestedCodeRelatedField(queryset=AssetVariant.objects.all())
    child_count = serializers.SerializerMethodField()
    is_parent = serializers.SerializerMethodField()
    is_child = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = (
            "id", "app", "app_name", "title", "actionbar", "cover_image", "parent",
            "orientation", "tag", "section", "status", "variant", "api_option",
            "sort_order", "created_at", "updated_at", "child_count", "is_parent", "is_child",
        )
        read_only_fields = ("id", "app_name", "created_at", "updated_at", "child_count", "is_parent", "is_child")

    def get_child_count(self, obj):
        return obj.children.count() if obj.parent_id is None else 0

    def get_is_parent(self, obj):
        return obj.children.exists()

    def get_is_child(self, obj):
        return obj.parent_id is not None

    def validate(self, attrs):
        category = self.instance or Category()
        for field, value in attrs.items():
            setattr(category, field, value)
        try:
            category.clean()
        except DjangoValidationError as exc:
            raise serializers.ValidationError(getattr(exc, "message_dict", exc.messages)) from exc
        return attrs