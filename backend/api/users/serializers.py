from djoser.serializers import (
    UserCreateSerializer,
    UserSerializer,
    serializers,
)
from django.contrib.auth import get_user_model

User = get_user_model()


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


class CustomUserSerializer(UserSerializer):
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
        read_only = (
            "id",
            "is_subscribed",
        )

    def get_is_subscribed(self, author):
        current_user = self.context.get("request").user
        if current_user.is_anonymous:
            return False
        return current_user.followers.filter(author=author).exists()
