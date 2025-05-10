from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from core.permissons import IsAuthorOrReadOnlyPermisson

from recipes.models import Recipe
from .serializers import RecipeSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (IsAuthorOrReadOnlyPermisson,)
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ("author",)
