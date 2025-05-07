from django.shortcuts import get_object_or_404
from rest_framework import serializers, validators
from django.contrib.auth import get_user_model
from rest_framework.relations import SlugRelatedField

from ingredients.models import Ingredient

User = get_user_model()


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ("id", "name", "measurement_unit")
