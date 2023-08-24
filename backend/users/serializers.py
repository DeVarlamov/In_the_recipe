from djoser.serializers import UserCreateSerializer
from drf_extra_fields.fields import Base64ImageField
from recipes.models import Recipe
from rest_framework import serializers

from .models import Subscribed, User


class UserRegistrationSerializer(UserCreateSerializer):
    """Сереалайзер регистрации"""
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('email',
                  'id',
                  'username',
                  'first_name',
                  'last_name',
                  'password',
                  )


class UserSerializer(serializers.ModelSerializer):
    """Сереалайзер данных юзера"""
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email',
                  'id',
                  'username',
                  'first_name',
                  'last_name',
                  'is_subscribed',
                  )

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        if user.is_anonymous:
            return False
        return Subscribed.objects.filter(user=user, author=obj).exists()


class RecipeSerializer(serializers.ModelSerializer):
    """Список рецептов без ингридиентов."""
    image = Base64ImageField(read_only=True)
    name = serializers.ReadOnlyField()
    cooking_time = serializers.ReadOnlyField()

    class Meta:
        model = Recipe
        fields = ('id', 'name',
                  'image', 'cooking_time')


class SubscribedSerializer(serializers.ModelSerializer):
    """Список обьектов на которые подписан юзер"""
    email = serializers.ReadOnlyField()
    username = serializers.ReadOnlyField()
    is_subscribed = serializers.SerializerMethodField()
    recipes = RecipeSerializer(many=True, read_only=True)
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed', 'recipes', 'recipes_count')

    def get_is_subscribed(self, obj):
        return (
            self.context.get('request').user.is_authenticated
            and Subscribed.objects.filter(user=self.context['request'].user,
                                          author=obj).exists()
        )

    def get_recipes_count(self, obj):
        return obj.recipes.count()


class SubscribeAuthorSerializer(SubscribedSerializer):
    """Подписка на автора и отписка."""

    def validate(self, obj):
        if self.context['request'].user == obj:
            raise serializers.ValidationError(
                {'errors': 'Нельзя подписаться на себя.'})
        return obj
