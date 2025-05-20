from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.user_reference import User
from users.models import Subscription

from .serializers import (
    AvatarSerializer,
    CreateSubscribeSerializer,
    SubscribtionSerializer,
)


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
        authors = User.objects.filter(subscribers__user=request.user)
        page = self.paginate_queryset(authors)
        serializer = CreateSubscribeSerializer(
            page, many=True, context={"request": request}
        )
        return self.get_paginated_response(serializer.data)

    @action(
        methods=("POST",),
        detail=True,
        permission_classes=(IsAuthenticated,),
        url_path="subscribe",
    )
    def subscribe(self, request, id):
        get_object_or_404(User, pk=id)
        serializer = SubscribtionSerializer(
            data={"author": id, "user": request.user.id},
            context={"request": request},
        )
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @subscribe.mapping.delete
    def unsubscribe(self, request, id):
        subscription_deleted, _ = Subscription.objects.filter(
            author=self.get_object(), user=request.user
        ).delete()
        if not subscription_deleted:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_204_NO_CONTENT)
