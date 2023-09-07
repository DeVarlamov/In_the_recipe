from djoser.serializers import UserCreateSerializer
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from api.v1.serializers import RecipeSerializer

from .models import Subscribed, User


class UserRegistrationSerializer(UserCreateSerializer):
    """Сереалайзер регистрации."""

    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'password',
        )


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для всех пользователей."""

    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
        )

    def get_is_subscribed(self, obj):
        """Метод получения подписки"""
        user = self.context.get('request').user
        return bool(
            user.is_authenticated
            and obj.subscribing.filter(user=user).exists()
        )


class SubscribedSerializer(UserSerializer):
    """Сереалайзер Подписок. для GET запроса"""

    recipes = serializers.SerializerMethodField(
        method_name='get_recipes', read_only=True
    )
    recipes_count = serializers.SerializerMethodField(
        method_name='get_recipes_count', read_only=True
    )

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + (
            'recipes',
            'recipes_count',
        )
        read_only_fields = (
            'email',
            'username',
            'last_name',
            'first_name',
        )

    def get_recipes_count(self, obj):
        """Метод получения колличества рецепта."""
        return obj.recipes.count()

    def get_recipes(self, object):
        """Метод получение рецепта."""
        try:
            limit = int(
                self.context['request'].query_params.get(
                    'recipes_limit', default=0
                )
            )
        except ValueError:
            raise ValueError('recipes_limit должен быть целым числом')
        author_recipes = object.recipes.all()[:limit]
        return RecipeSerializer(author_recipes, many=True).data


class AddSubscribedSerializer(serializers.ModelSerializer):
    """Сереалайзер добавления подписки"""

    class Meta:
        model = Subscribed
        fields = ('user', 'author')
        validators = [
            UniqueTogetherValidator(
                queryset=Subscribed.objects.all(),
                fields=['user', 'author'],
                message="Вы уже подписались ны пользователя",
            )
        ]

    def validate(self, attrs):
        user = attrs.get('user')
        author = attrs.get('author')

        if user == author:
            raise serializers.ValidationError(
                "Вы не можете подписаться на самого себя"
            )

        return attrs
