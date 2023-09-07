from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from requests import Response
from rest_framework import response, status
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny, IsAuthenticated

from .models import Subscribed, User
from .serializers import SubscribedSerializer, UserSerializer


class UsersViewSet(UserViewSet):
    """Эндотип Юзера."""

    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer
    pagination_class = LimitOffsetPagination
    pagination_class.default_limit = 3

    @action(
        detail=False, methods=['get'], permission_classes=(IsAuthenticated,)
    )
    def subscriptions(self, request):
        """Возвращает пользователей, на которых подписан текущий пользователь.
        В выдачу добавляются рецепты.
        """
        return self.get_paginated_response(
            SubscribedSerializer(
                self.paginate_queryset(
                    User.objects.filter(subscribing__user=request.user)
                ),
                many=True,
                context={'request': request},
            ).data
        )

    @action(
        detail=True, methods=['post'], permission_classes=(IsAuthenticated,)
    )
    def subscribe(self, request, **kwargs):
        """Подписываем  на пользователя.
        Доступно только авторизованным пользователям.
        """
        author_id = self.kwargs.get('id')
        author = get_object_or_404(User, id=author_id)
        serializer = SubscribedSerializer(
            author, data=request.data, context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return response.Response(
            serializer.data, status=status.HTTP_201_CREATED
        )

    @subscribe.mapping.delete
    def remove_from_subscribe(self, request, pk):
        """Метод удаления подписки"""
        get_object_or_404(Subscribed, user=request.user, recipe=pk).delete
        return Response(status=status.HTTP_204_NO_CONTENT)
