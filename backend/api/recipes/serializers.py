from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField

from recipes.models import Recipe, IngredientRecipe
from ingredients.models import Ingredient
from api.users.serializers import CustomUserSerializer


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

    def get_is_favorited(self, recipe):
        current_user = self.context.get("request").user
        if current_user.is_anonymous:
            return False
        return current_user.favorites.filter(recipe=recipe).exists()

    def get_is_in_shopping_cart(self, recipe):
        current_user = self.context.get("request").user
        if current_user.is_anonymous:
            return False
        return current_user.shopping_cart.filter(recipe=recipe).exists()

    def _save_ingredients(self, recipe, ingredients_data):
        if ingredients_data:
            IngredientRecipe.objects.bulk_create(
                [
                    IngredientRecipe(
                        recipe=recipe,
                        ingredient=Ingredient.objects.get(
                            id=item["ingredient"]["id"]
                        ),
                        amount=item["amount"],
                    )
                    for item in ingredients_data
                ]
            )

    def create(self, validated_data):
        ingredients_data = validated_data.pop("ingredient_recipes", None)
        recipe = Recipe.objects.create(
            author=self.context["request"].user, **validated_data
        )
        self._save_ingredients(recipe, ingredients_data)
        return recipe

    def update(self, instance, validated_data):
        ingredients_data = validated_data.pop("ingredient_recipes", None)
        instance.ingredients.clear()
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        self._save_ingredients(instance, ingredients_data)
        return instance


class ShortRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ("id", "name", "image", "cooking_time")
