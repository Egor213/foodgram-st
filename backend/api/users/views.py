from djoser.views import UserViewSet
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializers import AvatarSerializer
from users.models import Subscription
from django.contrib.auth import get_user_model

from .serializers import SubscribeAuthorSerializer

User = get_user_model()


class CustomUserViewSet(UserViewSet):
    @action(
        methods=("PUT",),
        detail=False,
        permission_classes=(IsAuthenticated,),
        url_path="me/avatar",
    )
    def avatar(self, request):
        data = request.data
        if "avatar" not in request.data:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        serializer = self._set_avatar(request.user, data)
        return Response(serializer.data)

    @avatar.mapping.delete
    def delete_avatar(self, request):
        self._set_avatar(request.user, {"avatar": None})
        return Response(status=status.HTTP_204_NO_CONTENT)

    def _set_avatar(self, user, data):
        serializer = AvatarSerializer(user, data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return serializer

    @action(
        methods=("GET",),
        detail=False,
        permission_classes=(IsAuthenticated,),
        url_path="me",
    )
    def me(self, request, *args, **kwargs):
        return super().me(request, *args, **kwargs)

    @action(
        methods=("GET",),
        detail=False,
        permission_classes=(IsAuthenticated,),
        url_path="subscriptions",
    )
    def subscriptions(self, request):
        authors = User.objects.filter(followings__user=request.user)
        page = self.paginate_queryset(authors)
        serializer = SubscribeAuthorSerializer(
            page, many=True, context={"request": request}
        )
        return self.get_paginated_response(serializer.data)

    # @action(
    #     methods=("POST",),
    #     detail=True,
    #     permission_classes=(IsAuthenticated,),
    #     url_path="subscribe",
    # )
    # def subscribe(self, request, id):
    #     print(id)
    #     return Response()
