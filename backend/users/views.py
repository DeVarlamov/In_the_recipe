from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from users.serializers import FollowSerializer
from requests import Response
from users.models import Subscribed, User
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.permissions import IsAuthenticated


class UserViewSet(UserViewSet):

    @action(
        detail=True,
        permission_classes=[IsAuthenticated],
        methods=['POST', 'DELETE'],
        )
    def get_subscribed(self, request, id):
        user = request.user
        author = get_object_or_404(User, id=id)

        if self.request.method == 'POST':
            if Subscribed.objects.filter(user=user, author=author):
                return Response({'Вы уже подписались на этого атора'},
                                status=status.HTTP_400_BAD_REQUEST)
            if user == author:
                return Response({'Не будь нарцисом'},
                                status=status.HTTP_400_BAD_REQUEST)
            fallow = Subscribed.objects.create(user=user, author=author)
            serializer = FollowSerializer(
                fallow, context={'request': request},
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if Subscribed.objects.filter(user=user, author=author):
            follow = get_object_or_404(Subscribed, user=user, author=author)
            follow.delete()
        return Response('Подписка удаленна',
                        status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False,
        permission_classes=[IsAuthenticated],
        methods=['GET'],
    )
    def subscribed(self, request):
        user = request.user
        queryset = Subscribed.objects.filter(user=user)
        pages = self.paginate_queryset(queryset)
        serializer = FollowSerializer(
            pages,
            many=True,
            context={'request': request},
        )
        return self.get_paginated_response(serializer.data)
