from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from users.serializers import FollowSerializer
from requests import Response
from users.models import Following, User
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.permissions import IsAuthenticated


class UserViewSet(UserViewSet):

    @action(
        detail=True,
        permission_classes=[IsAuthenticated],
        methods=['POST', 'DELETE'],
        )
    def fallowing(self, request, id):
        user = request.user
        author = get_object_or_404(User, id=id)
        if self.request.method == 'POST':
            if Following.objects.filter(user=user, author=author):
                return Response({'Вы уже подписались на этого атора'},
                                status=status.HTTP_400_BAD_REQUEST)
            if user == author:
                return Response({'Не будь нарцисом'},
                                status=status.HTTP_400_BAD_REQUEST)
            fallow = Following.objects.create(user=user, author=author)
            serializer = FollowSerializer(
                fallow, context={'request': request},
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if Following.objects.filter(user=user, author=author):
            follow = get_object_or_404(Following, user=user, author=author)
            follow.delete()
            return Response('Подписка удаленна',
                            status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False,
        permission_classes=[IsAuthenticated],
        methods=['GET'],
    )
    def followings(self, request):
        user = request.user
        queryset = Following.objects.filter(user=user)
        pages = self.paginate_queryset(queryset)
        serializer = FollowSerializer(
            pages,
            many=True,
            context={'request': request},
        )
        return self.get_paginated_response(serializer.data)
