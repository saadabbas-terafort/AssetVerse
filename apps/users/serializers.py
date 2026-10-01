from rest_framework import serializers

from .models import PublicUser, PublicUserToken, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email", "first_name", "last_name", "is_active")


class PublicUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = PublicUser
        fields = "__all__"


class PublicUserTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = PublicUserToken
        fields = "__all__"