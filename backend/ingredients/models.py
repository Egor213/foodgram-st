from django.db import models


class Ingredient(models.Model):
    name = models.CharField("Название", max_length=128, db_index=True)
    measurement_unit = models.CharField("Единицы измерения", max_length=64)

    class Meta:
        verbose_name = "Ингредиент"
        verbose_name_plural = "Ингредиенты"
        ordering = ("name",)
        constraints = [
            models.UniqueConstraint(
                fields=("name", "measurement_unit"),
                name="name_measurement_unit",
            )
        ]

    def __str__(self):
        return f"{self.name} ({self.measurement_unit})"
