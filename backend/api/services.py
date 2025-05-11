import os
from io import BytesIO

from django.conf import settings
from fpdf import FPDF
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from recipes.models import Recipe, ShoopingCart

from .recipes.serializers import RecipeSerializer


def get_user_shopping_cart(user):
    return [recipe.recipe for recipe in ShoopingCart.objects.filter(user=user)]


def formated_recipes(request):
    recipes = get_user_shopping_cart(request.user)
    serializer = RecipeSerializer(
        recipes, many=True, context={"request": request}
    )
    return serializer.data


class PDFBuilder:
    def __init__(self, data):
        self.data = data
        self.pdf = FPDF()
        self.pdf.add_page()

        font_path_normal = os.path.join(
            settings.STATIC_ROOT, "fonts", "DejaVuSans.ttf"
        )
        font_path_bold = os.path.join(
            settings.STATIC_ROOT, "fonts", "DejaVuSans-Bold.ttf"
        )
        self.pdf.add_font("DejaVu", "", font_path_normal, uni=True)
        self.pdf.add_font("DejaVu", "B", font_path_bold, uni=True)
        self.pdf.set_font("DejaVu", size=12)

    def build(self):
        self._add_header("Список покупок", font_size=16, style="B", align="C")
        self.pdf.ln(10)

        all_ingredients = []

        for recipe in self.data:
            self._add_recipe(recipe, all_ingredients)
            self.pdf.ln(10)

        self._add_ingredient_list(all_ingredients)

        pdf_bytes = self.pdf.output(dest="S").encode(
            "latin-1", errors="ignore"
        )
        return BytesIO(pdf_bytes)

    def _add_header(self, text, font_size=12, style="", align="L"):
        self.pdf.set_font("DejaVu", style, font_size)
        self.pdf.cell(0, 10, text, ln=True, align=align)
        self.pdf.set_font("DejaVu", "", 12)

    def _add_recipe(self, recipe, all_ingredients):
        self._add_header(f"Рецепт: {recipe['name']}", font_size=14, style="B")

        author = recipe["author"]
        self._add_line(
            (
                f"Автор: {author['first_name']} "
                f"{author['last_name']} ({author['username']})"
            )
        )
        self._add_line(f"Время приготовления: {recipe['cooking_time']} мин")
        self.pdf.multi_cell(0, 8, f"Описание: {recipe['text']}")
        self.pdf.ln(5)

        self._add_header("Ингредиенты:", font_size=12, style="B")
        for ingredient in recipe["ingredients"]:
            line = self._format_ingredient(ingredient)
            self._add_line(line)
            all_ingredients.append(ingredient)

    def _add_line(self, text):
        self.pdf.cell(0, 8, text, ln=True)

    def _format_ingredient(self, ingredient):
        return (
            f"- {ingredient['name']} "
            f"— {ingredient['amount']} "
            f"{ingredient['measurement_unit']}"
        )

    def _add_ingredient_list(self, all_ingredients):
        self.pdf.ln(10)
        self._add_header(
            "Список всех ингредиентов для покупок:", font_size=14, style="B"
        )

        seen = set()
        unique_lines = []
        for ingredient in all_ingredients:
            key = (
                ingredient["name"],
                ingredient["measurement_unit"],
            )
            if key not in seen:
                seen.add(key)
                line = self._format_ingredient(ingredient)
                unique_lines.append(line)

        for line in unique_lines:
            self._add_line(line)


def generate_recipes_pdf(request):
    recipes = formated_recipes(request)
    pdf_builder = PDFBuilder(recipes)
    return pdf_builder.build()


def is_related(user, obj, related_manager_name, lookup_field="recipe"):
    if (
        not user
        or not hasattr(user, related_manager_name)
        or user.is_anonymous
    ):
        return False
    manager = getattr(user, related_manager_name)
    filter_kwargs = {lookup_field: obj}
    return manager.filter(**filter_kwargs).exists()


def add_to_related_model(request, pk, serializer_class):
    get_object_or_404(Recipe, pk=pk)
    serializer = serializer_class(
        data={"recipe": pk, "user": request.user.id},
        context={"request": request},
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)


def delete_from_related_model(request, pk, model_class):
    recipe = get_object_or_404(Recipe, pk=pk)
    deleted, _ = model_class.objects.filter(
        recipe=recipe, user=request.user
    ).delete()
    if not deleted:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_204_NO_CONTENT)
