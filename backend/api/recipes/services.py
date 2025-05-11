from recipes.models import ShoopingCart
from .serializers import RecipeSerializer
from io import BytesIO
from fpdf import FPDF
from django.conf import settings
import os


def get_user_shopping_cart(user):
    return [recipe.recipe for recipe in ShoopingCart.objects.filter(user=user)]


def formated_recipes(request):
    recipes = get_user_shopping_cart(request.user)
    serializer = RecipeSerializer(
        recipes, many=True, context={"request": request}
    )
    return serializer.data


from fpdf import FPDF
from io import BytesIO
import os
from django.conf import settings


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
        self.pdf.set_font("DejaVu", "B", 16)
        self.pdf.cell(0, 10, "Список покупок", ln=True, align="C")
        self.pdf.ln(10)

        for recipe in self.data:
            self._add_recipe(recipe)
            self.pdf.ln(10)

        pdf_bytes = self.pdf.output(dest="S").encode(
            "latin-1", errors="ignore"
        )
        pdf_buffer = BytesIO(pdf_bytes)
        pdf_buffer.seek(0)
        return pdf_buffer

    def _add_recipe(self, recipe):
        self.pdf.set_font("DejaVu", "B", 14)
        self.pdf.cell(0, 10, f"Рецепт: {recipe['name']}", ln=True)

        author = recipe["author"]
        self.pdf.set_font("DejaVu", "", 12)
        self.pdf.cell(
            0,
            8,
            f"Автор: {author['first_name']} {author['last_name']} ({author['username']})",
            ln=True,
        )

        self.pdf.cell(
            0, 8, f"Время приготовления: {recipe['cooking_time']} мин", ln=True
        )
        self.pdf.multi_cell(0, 8, f"Описание: {recipe['text']}")

        self.pdf.set_font("DejaVu", "B", 12)
        self.pdf.cell(0, 8, "Ингредиенты:", ln=True)

        self.pdf.set_font("DejaVu", "", 12)
        for ingredient in recipe["ingredients"]:
            line = f"- {ingredient['name']} — {ingredient['amount']} {ingredient['measurement_unit']}"
            self.pdf.cell(0, 8, line, ln=True)


def generate_recipes_pdf(request):
    recipes = formated_recipes(request)
    pdf_builder = PDFBuilder(recipes)
    return pdf_builder.build()
