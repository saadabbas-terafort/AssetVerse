from rest_framework import serializers

from apps.app_settings.models import AppSetting


class ActiveCodeRelatedField(serializers.RelatedField):
    def to_internal_value(self, data):
        if not isinstance(data, str) or not data:
            raise serializers.ValidationError("Lookup values must be submitted as codes.")
        instance = self.queryset.filter(code=data, is_active=True).first()
        if instance is None:
            raise serializers.ValidationError(f"Unknown or inactive lookup code: {data}.")
        return instance

    def to_representation(self, value):
        return value.code


class NestedCodeRelatedField(ActiveCodeRelatedField):
    def to_representation(self, value):
        return {"code": value.code, "label": value.label}


class AppSlugField(serializers.RelatedField):
    queryset = AppSetting.objects.all()

    def to_internal_value(self, data):
        if not isinstance(data, str) or not data:
            raise serializers.ValidationError("App must be an active app slug.")
        app = AppSetting.objects.filter(slug=data, is_active=True).first()
        if app is None:
            raise serializers.ValidationError("Unknown or inactive app slug.")
        return app

    def to_representation(self, value):
        return {"slug": value.slug, "label": value.label}