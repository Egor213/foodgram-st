from djoser.serializers import UserCreateSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model


class CustomCreateUserSerializer(UserCreateSerializer):
    class Meta:
        model = get_user_model()
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
