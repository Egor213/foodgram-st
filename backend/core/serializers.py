from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from core.user_reference import User


class AvatarSerializer(serializers.ModelSerializer):
    avatar = Base64ImageField(allow_null=True, required=False)

    class Meta:
        model = User
        fields = ("avatar",)
