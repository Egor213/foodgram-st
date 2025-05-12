import json

from django.core.management.base import BaseCommand

from ingredients.models import Ingredient


class Command(BaseCommand):
    help = "Импортирует ингредиенты из JSON-файла"

    def add_arguments(self, parser):
        parser.add_argument("file_path", type=str, help="Путь к JSON-файлу")

    def handle(self, *args, **options):
        file_path = options["file_path"]
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
            Ingredient.objects.bulk_create(
                [
                    Ingredient(
                        name=item["name"],
                        measurement_unit=item["measurement_unit"],
                    )
                    for item in data
                ],
                ignore_conflicts=True,
            )
        self.stdout.write(self.style.SUCCESS("Ингредиенты успешно загружены"))
