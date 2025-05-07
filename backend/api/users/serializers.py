from djoser.serializers import UserCreateSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model


class CustomCreateUserSerializer(UserCreateSerializer):
    # id = serializers.PrimaryKeyRelatedField(read_only=True)
    # email = serializers.EmailField(required=True)
    # password = serializers.CharField(required=True, write_only=True)
    # first_name = serializers.CharField(required=True, max_length=150)
    # last_name = serializers.CharField(required=True, max_length=150)

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
