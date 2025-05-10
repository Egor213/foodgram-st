from djoser.serializers import UserCreateSerializer, UserSerializer
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
    class Meta:
        model = User
        fields = "__all__"
