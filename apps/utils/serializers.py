from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers


class AssetValidationMixin:
    variant_code = None

    def validate(self, attrs):
        instance = self.instance or self.Meta.model()
        for field, value in attrs.items():
            if field != "tags":
                setattr(instance, field, value)
        try:
            instance.clean()
        except DjangoValidationError as exc:
            raise serializers.ValidationError(getattr(exc, "message_dict", exc.messages)) from exc
        return attrs