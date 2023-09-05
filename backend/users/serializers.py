from api.v1.serializers import RecipeSerializer, UserDateSerializer
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions as django_exceptions
from djoser.serializers import UserCreateSerializer
from rest_framework import exceptions, serializers, status

from .models import Subscribed, User


class UserRegistrationSerializer(UserCreateSerializer):
    """Сереалайзер регистрации."""

    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('email',
                  'id',
                  'username',
                  'first_name',
                  'last_name',
                  'password',
                  )


class UsersSerializer(serializers.ModelSerializer):
    """Сериализатор для всех пользователей."""

    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'username',
                  'first_name', 'last_name', 'is_subscribed',)

    def get_is_subscribed(self, author):
        """Проверка подписки пользователей."""
        request = self.context.get('request')
        return (request and request.user.is_authenticated
                and request.user.follower.filter(author=author).exists())


class SubscribedSerializer(UserDateSerializer):
    """Сереалайзер Подписок."""
    recipes = serializers.SerializerMethodField(method_name='get_recipes',
                                                read_only=True)
    recipes_count = serializers.SerializerMethodField(
        method_name='get_recipes_count', read_only=True)

    class Meta(UserDateSerializer.Meta):
        fields = UserDateSerializer.Meta.fields + (
            'recipes', 'recipes_count',
        )
        read_only_fields = ('email', 'username', 'last_name', 'first_name',)

    def validate(self, data):
        """Валидация подписки."""
        author = self.instance
        user = self.context.get('request').user
        if Subscribed.objects.filter(user=user, author=author).exists():
            raise exceptions.ValidationError(
                detail='Вы уже подписаны на этого пользователя!',
                code=status.HTTP_400_BAD_REQUEST
            )
        if user == author:
            raise exceptions.ValidationError(
                detail='Нельзя подписываться на себя',
                code=status.HTTP_400_BAD_REQUEST
            )
        return data

    def get_recipes_count(self, obj):
        """Метод получения колличества рецепта."""
        return obj.recipes.count()

    def get_recipes(self, object):
        """Метод получение рецепта."""
        limit = int(self.context['request'].query_params.get(
            'recipes_limit', default=0)
        )
        author_recipes = object.recipes.all()[:limit]
        return RecipeSerializer(
            author_recipes, many=True
        ).data

    def get_is_subscribed(self, obj):
        """Метод получения подписок ."""
        user = self.context.get('request').user
        return (
            user.is_authenticated
            and obj.subscribing.filter(user=user).exists()
        )


class SubscribeAuthorSerializer(SubscribedSerializer):
    """Подписка на автора и отписка."""
    email = serializers.ReadOnlyField()
    username = serializers.ReadOnlyField()
    last_name = serializers.ReadOnlyField()
    first_name = serializers.ReadOnlyField()

    def validate(self, obj):
        if self.context['request'].user == obj:
            raise serializers.ValidationError(
                {'errors': 'Нельзя подписаться на себя.'})
        return obj
