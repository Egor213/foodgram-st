from django.contrib import admin
from .models import Ingredient


@admin.register(Ingredient)
class RecipeAdmin(admin.ModelAdmin):
    pass
