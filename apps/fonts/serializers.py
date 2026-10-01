from rest_framework import serializers

from .models import Font


class FontSerializer(serializers.ModelSerializer):
    class Meta:
        model = Font
        fields = "__all__"