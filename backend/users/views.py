from api.v1.serializers import UserDateSerializer
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import response, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated

from .models import Subscribed, User
from .serializers import SubscribedSerializer, UsersSerializer


class UsersViewSet(UserViewSet):
    """Эндотип Юзера."""

    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UsersSerializer

    @action(detail=False, methods=['get'],
            permission_classes=(IsAuthenticated,))
    def subscriptions(self, request):
        """Возвращает пользователей, на которых подписан текущий пользователь.
        В выдачу добавляются рецепты.
        """
        return self.get_paginated_response(
            SubscribedSerializer(
                self.paginate_queryset(
                    User.objects.filter(following__user=request.user)
                ),
                many=True,
                context={'request': request},
            ).data
        )

    @action(detail=True, methods=['post', 'delete'],
            permission_classes=(IsAuthenticated,))
    def subscribe(self, request, **kwargs):
        """Подписываем / отписываемся на пользователя.
        Доступно только авторизованным пользователям.
        """
        user = request.user
        author_id = self.kwargs.get('id')
        author = get_object_or_404(User, id=author_id)
        if request.method == 'POST':
            serializer = SubscribedSerializer(author,
                                              data=request.data,
                                              context={'request': request})
            serializer.is_valid(raise_exception=True)
            Subscribed.objects.create(user=user, author=author)
            return response.Response(serializer.data,
                                     status=status.HTTP_201_CREATED)
        get_object_or_404(Subscribed, user=user, author=author).delete()
        return response.Response(status=status.HTTP_204_NO_CONTENT)
