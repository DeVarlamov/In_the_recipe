from djoser.views import UserViewSet
from rest_framework import response, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated

from users.pagination import LimitPageNumberPagination

from .models import Subscribed, User
from .serializers import (
    AddSubscribedSerializer,
    SubscribedSerializer,
    UserSerializer,
)


class UsersViewSet(UserViewSet):
    """Эндотип Юзера."""

    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer
    pagination_class = LimitPageNumberPagination

    @staticmethod
    def adding_author(add_serializer, model, request, author_id):
        """Кастомный метод добавления author и получения данных"""
        user = request.user
        data = {'user': user.id, 'author': author_id}
        serializer = add_serializer(data=data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response_data = {
            'email': user.email,
            'id': user.id,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
        }
        recipes = serializer.data.get('recipes', [])
        for recipe_data in recipes:
            recipe_id = recipe_data.get('id')
            recipe_name = recipe_data.get('name')
            recipe_image = recipe_data.get('image')
            recipe_cooking_time = recipe_data.get('cooking_time')
            recipe = {
                'id': recipe_id,
                'name': recipe_name,
                'image': recipe_image,
                'cooking_time': recipe_cooking_time,
            }
            response_data['recipes'].append(recipe)
        response_data['recipes_count'] = len(recipes)

        return response.Response(response_data, status=status.HTTP_201_CREATED)

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
        detail=True, methods=['post'], permission_classes=[IsAuthenticated]
    )
    def subscribe(self, request, id):
        """Подписываем пользователя.
        Доступно только авторизованным пользователям.
        """
        return self.adding_author(
            AddSubscribedSerializer, Subscribed, request, id
        )

    @subscribe.mapping.delete
    def delete_subscribe(self, request, id):
        """Отписываемся от пользователя."""
        Subscribed.objects.filter(user=request.user, author=id).delete()
        return response.Response(
            {'detail': 'Подписка удалена'}, status=status.HTTP_204_NO_CONTENT
        )
