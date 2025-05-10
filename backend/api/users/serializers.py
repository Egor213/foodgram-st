from djoser.serializers import (
    UserCreateSerializer,
    UserSerializer,
)
from django.contrib.auth import get_user_model
from rest_framework import serializers
from core.serializers import AvatarSerializer
from rest_framework.validators import UniqueTogetherValidator

User = get_user_model()


class CustomCreateUserSerializer(UserCreateSerializer):
    password = serializers.CharField(write_only=True)

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
        read_only_fields = ("id",)


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
            "avatar",
        )
        read_only_fields = ("id", "is_subscribed")

    def get_is_subscribed(self, author):
        current_user = self.context.get("request").user
        if current_user.is_anonymous:
            return False
        return current_user.followers.filter(author=author).exists()


class SubscribeAuthorSerializer(CustomUserSerializer):
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta(CustomUserSerializer.Meta):
        fields = (
            "email",
            "id",
            "username",
            "first_name",
            "last_name",
            "is_subscribed",
            "recipes",
            "recipes_count",
            "avatar",
        )

    def get_recipes(self, obj):
        from api.recipes.serializers import ShortRecipeSerializer

        recipes = obj.recipes.all()
        request = self.context.get("request")
        return ShortRecipeSerializer(
            recipes, many=True, context={"request": request}
        ).data

    def get_recipes_count(self, obj):
        return obj.recipes.all().count()
