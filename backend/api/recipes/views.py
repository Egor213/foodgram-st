from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from core.permissons import IsAuthorOrReadOnlyPermisson

from recipes.models import Recipe
from .serializers import RecipeSerializer
from short_urls.models import ShortUrl


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (IsAuthorOrReadOnlyPermisson,)
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ("author",)

    @action(
        methods=("GET",),
        detail=True,
        url_path="get-link",
        url_name="get-link",
    )
    def get_short_url(self, request, pk=None):
        origin_url = f"/api/recipes/{pk}/"
        short_url_instance, _ = ShortUrl.objects.get_or_create(
            origin_url=origin_url
        )
        return Response(
            {
                "short-link": request.build_absolute_uri(
                    short_url_instance.short_url
                )
            }
        )
