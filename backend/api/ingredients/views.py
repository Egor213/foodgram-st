from rest_framework import viewsets, filters
from rest_framework.permissions import AllowAny
from ingredients.models import Ingredient

from .serializers import IngredientSerializer


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)
    permission_classes = (AllowAny,)
