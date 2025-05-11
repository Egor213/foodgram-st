from django.conf import settings
from django.http import FileResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.services import (
    add_to_related_model,
    delete_from_related_model,
    generate_recipes_pdf,
)
from core.permissons import IsAuthorOrReadOnlyPermisson
from recipes.models import FavoriteRecipe, Recipe, ShoopingCart
from short_urls.models import ShortUrl

from .filters import ProductFilter
from .serializers import (
    FavoriteRecipeSeraializer,
    RecipeSerializer,
    ShoppingCartSeraializer,
)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (IsAuthorOrReadOnlyPermisson,)
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ("author",)
    filterset_class = ProductFilter

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

    @action(
        methods=("POST",),
        detail=True,
        permission_classes=(IsAuthenticated,),
        url_path="shopping_cart",
    )
    def shopping_cart(self, request, pk):
        return add_to_related_model(request, pk, ShoppingCartSeraializer)

    @shopping_cart.mapping.delete
    def delete_shopping_cart(self, request, pk):
        return delete_from_related_model(request, pk, ShoopingCart)

    @action(
        methods=("POST",),
        detail=True,
        permission_classes=(IsAuthenticated,),
        url_path="favorite",
    )
    def favorite_recipe(self, request, pk):
        return add_to_related_model(request, pk, FavoriteRecipeSeraializer)

    @favorite_recipe.mapping.delete
    def delete_favorite_recipe(self, request, pk):
        return delete_from_related_model(request, pk, FavoriteRecipe)

    @action(
        methods=("GET",),
        detail=False,
        permission_classes=(IsAuthenticated,),
        url_path="download_shopping_cart",
    )
    def download_shopping_cart(self, request):
        return FileResponse(
            generate_recipes_pdf(request),
            as_attachment=True,
            filename=f"{settings.NAME_SHOPPING_CART_LIST_FILE}.pdf",
        )
