from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from core.permissons import IsAuthorOrReadOnlyPermisson
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.http import FileResponse
from django.conf import settings

from .services import generate_recipes_pdf
from recipes.models import Recipe, ShoopingCart
from .serializers import RecipeSerializer, ShoppingCartSeraializer
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

    @action(
        methods=("POST",),
        detail=True,
        permission_classes=(IsAuthenticated,),
        url_path="shopping_cart",
    )
    def shopping_cart(self, request, pk):
        serializer = ShoppingCartSeraializer(
            data={"recipe": pk, "user": request.user.id},
            context={"request": request},
        )
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @shopping_cart.mapping.delete
    def delete_shopping_cart(self, request, pk=None):
        shopping_cart_delete, _ = ShoopingCart.objects.filter(
            recipe=pk, user=request.user
        ).delete()
        if not shopping_cart_delete:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_204_NO_CONTENT)

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
