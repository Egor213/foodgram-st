from djoser.serializers import (
    UserCreateSerializer,
    UserSerializer,
)
from django.contrib.auth import get_user_model
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

User = get_user_model()


class AvatarSerializer(serializers.ModelSerializer):
    avatar = Base64ImageField(allow_null=True, required=False)

    class Meta:
        model = User
        fields = ("avatar",)


class CustomCreateUserSerializer(UserCreateSerializer):
    class Meta:
        model = User
        fields = (
            "email",
            "id",
            "username",
            "first_name",
            "last_name",
            "password",
        )
        read_only = ("id",)
        write_only = ("password",)


class CustomUserSerializer(AvatarSerializer, UserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "email",
            "id",
            "username",
            "first_name",
            "last_name",
            "is_subscribed",
        ) + AvatarSerializer.Meta.fields
        read_only = (
            "id",
            "is_subscribed",
        )

    def get_is_subscribed(self, author):
        current_user = self.context.get("request").user
        if current_user.is_anonymous:
            return False
        return current_user.followers.filter(author=author).exists()
