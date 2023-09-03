from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .models import Subscribed, User
from .serializers import (
    SubscribeAuthorSerializer,
    UserCreateSerializer,
    UserSerializer,
)


class UserViewSet(UserViewSet):
    """Эндотип Юзера."""

    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def get_serializer_class(self):
        """Получение сереалайзера."""
        if self.action in ('list', 'retrieve'):
            return UserSerializer
        return UserCreateSerializer

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
