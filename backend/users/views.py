from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.mixins import (
    CreateModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .models import Subscribed, User
from .serializers import (
    SetPasswordSerializer,
    SubscribeAuthorSerializer,
    SubscribedSerializer,
    UserCreateSerializer,
    UserSerializer,
)


class CreateListRetriveViewSet(
    CreateModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    pass


class UsersViewSet(CreateListRetriveViewSet):
    """Эндотип Юзера."""

    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def get_serializer_class(self):
        """Получение сереалайзера."""
        if self.action in ('list', 'retrieve'):
            return UserSerializer
        return UserCreateSerializer

    @action(detail=False, methods=['get'], pagination_class=None,
            permission_classes=(IsAuthenticated,))
    def me(self, request):
        """Метод получения профиля текущего пользователяю."""
        serializer = UserSerializer(request.user, context={'request': request})
        return Response(serializer.data,
                        status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'],
            permission_classes=[IsAuthenticated])
    def set_password(self, request):
        serializer = SetPasswordSerializer(request.user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {'detail': 'Пароль успешно изменен!'},
            status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'],
            permission_classes=(IsAuthenticated,))
    def subscriptions(self, request):
        queryset = self.get_queryset().filter(subscribing__user=request.user)
        page = self.paginate_queryset(queryset)
        serializer = SubscribedSerializer(page, many=True,
                                          context={'request': request})
        return self.get_paginated_response(serializer.data)

    @action(detail=True, methods=['post', 'delete'],
            permission_classes=(IsAuthenticated,))
    def subscribe(self, request, **kwargs):
        author = get_object_or_404(User, id=kwargs['pk'])
        serializer = SubscribeAuthorSerializer(author, data=request.data,
                                               context={'request': request})

        if serializer.is_valid(raise_exception=True):
            if request.method == 'POST':
                if Subscribed.objects.filter(user=request.user,
                                             author=author).exists():
                    raise ValidationError('Вы уже подписаны на этого автора')
                if author == request.user:
                    raise ValidationError(
                        'Вы не можете подписаться на самого себя')
                Subscribed.objects.create(user=request.user, author=author)
                return Response(serializer.data,
                                status=status.HTTP_201_CREATED)
            if request.method == 'DELETE':
                try:
                    subscribed = Subscribed.objects.get(user=request.user,
                                                        author=author)
                except Subscribed.DoesNotExist:
                    raise ValidationError('Вы не подписаны на этого автора')
                subscribed.delete()
                return Response({'detail': 'Успешная отписка'},
                                status=status.HTTP_204_NO_CONTENT)
        return None
