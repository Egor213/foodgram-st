from django.db import transaction
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from api.users.serializers import CustomUserSerializer
from ingredients.models import Ingredient
from recipes.models import (
    FavoriteRecipe,
    IngredientRecipe,
    Recipe,
    ShoopingCart,
)


class IngredientRecipeSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source="ingredient.id")
    name = serializers.CharField(source="ingredient.name", read_only=True)
    measurement_unit = serializers.CharField(
        source="ingredient.measurement_unit", read_only=True
    )
    amount = serializers.IntegerField(min_value=1)

    class Meta:
        model = IngredientRecipe
        fields = ("id", "name", "measurement_unit", "amount")


class RecipeSerializer(serializers.ModelSerializer):
    image = Base64ImageField()
    ingredients = IngredientRecipeSerializer(
        many=True, source="ingredient_recipes"
    )
    author = CustomUserSerializer(read_only=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            "id",
            "author",
            "ingredients",
            "is_favorited",
            "is_in_shopping_cart",
            "name",
            "image",
            "text",
            "cooking_time",
        )
        read_only_fields = ("is_favorited", "is_in_shopping_cart")

    def validate_image(self, image):
        if not image:
            raise serializers.ValidationError("Изображение обязательно.")
        return image

    def validate(self, attrs):
        ingredients = attrs.get("ingredient_recipes", [])
        if not len(ingredients):
            raise serializers.ValidationError(
                "Должен быть указан хотя бы один ингредиент."
            )
        return super().validate(attrs)

    def validate_ingredients(self, ingredients):
        if not ingredients:
            raise serializers.ValidationError(
                "Укажите хотя бы один ингредиент."
            )

        ingredient_ids = [
            ingredient["ingredient"]["id"] for ingredient in ingredients
        ]
        if len(ingredient_ids) != len(set(ingredient_ids)):
            raise serializers.ValidationError(
                "Ингредиенты не должны повторяться."
            )

        missing_ids = [
            ingredient_id
            for ingredient_id in ingredient_ids
            if not Ingredient.objects.filter(id=ingredient_id).exists()
        ]
        if missing_ids:
            raise serializers.ValidationError(
                f"Ингредиенты с id={missing_ids} не существуют."
            )
        return ingredients

    def _is_related(self, recipe, relation_name):
        current_user = self.context.get("request").user
        if current_user.is_anonymous:
            return False
        return (
            getattr(current_user, relation_name).filter(recipe=recipe).exists()
        )

    def get_is_favorited(self, recipe):
        return self._is_related(recipe, "favorites")

    def get_is_in_shopping_cart(self, recipe):
        return self._is_related(recipe, "shopping_cart")

    def _save_ingredients(self, recipe, ingredients_data):
        IngredientRecipe.objects.bulk_create(
            [
                IngredientRecipe(
                    recipe=recipe,
                    ingredient_id=item["ingredient"]["id"],
                    amount=item["amount"],
                )
                for item in ingredients_data
            ]
        )

    @transaction.atomic
    def create(self, validated_data):
        ingredients_data = validated_data.pop("ingredient_recipes", None)
        validated_data["author"] = self.context["request"].user
        recipe = super().create(validated_data)
        self._save_ingredients(recipe, ingredients_data)
        return recipe

    @transaction.atomic
    def update(self, instance, validated_data):
        ingredients_data = validated_data.pop("ingredient_recipes", None)
        instance.ingredients.clear()
        instance = super().update(instance, validated_data)
        self._save_ingredients(instance, ingredients_data)
        return instance


class ShortRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ("id", "name", "image", "cooking_time")


class BaseShoppingFavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("user", "recipe")
        abstract = True

    @classmethod
    def build_validator(cls, model_class, message):
        return [
            UniqueTogetherValidator(
                queryset=model_class.objects.all(),
                fields=("recipe", "user"),
                message=message,
            )
        ]

    def to_representation(self, instance):
        return ShortRecipeSerializer(
            instance.recipe, context=self.context
        ).data


class ShoppingCartSeraializer(BaseShoppingFavoriteSerializer):
    class Meta(BaseShoppingFavoriteSerializer.Meta):
        model = ShoopingCart
        validators = BaseShoppingFavoriteSerializer.build_validator(
            ShoopingCart, "Рецепт уже добавлен в корзину"
        )


class FavoriteRecipeSeraializer(BaseShoppingFavoriteSerializer):
    class Meta(BaseShoppingFavoriteSerializer.Meta):
        model = FavoriteRecipe
        validators = BaseShoppingFavoriteSerializer.build_validator(
            FavoriteRecipe, "Рецепт уже добавлен в избранное"
        )
