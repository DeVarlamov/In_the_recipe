from django.contrib.auth.password_validation import validate_password
from django.core import exceptions as django_exceptions
from djoser.serializers import UserCreateSerializer
from recipes.models import Recipe
from rest_framework import serializers

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


class UserSerializer(serializers.ModelSerializer):
    """Сереалайзер данных юзера."""

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


class SetPasswordSerializer(serializers.Serializer):
    """Сереализатор изменение пароля пользователя."""

    current_password = serializers.CharField()
    new_password = serializers.CharField()

    def validate(self, data):
        try:
            validate_password(data['new_password'])
        except django_exceptions.ValidationError as e:
            raise serializers.ValidationError(
                {'new_password': list(e.messages)})
        return data

    def update(self, instance, validated_data):
        current_password = validated_data['current_password']
        new_password = validated_data['new_password']
        if not instance.check_password(current_password):
            raise serializers.ValidationError(
                {'current_password': 'Неправильный пароль.'})
        if current_password == new_password:
            raise serializers.ValidationError(
                {'new_password': 'Новый пароль должен отличаться от текущего.',
                 })
        instance.set_password(new_password)
        instance.save()
        return validated_data


class RecipeSerializer(serializers.ModelSerializer):
    """Список рецептов без ингридиентов."""

    image = serializers.ReadOnlyField(source='image.url')
    name = serializers.ReadOnlyField()
    cooking_time = serializers.ReadOnlyField()

    class Meta:
        model = Recipe
        fields = ('id', 'name',
                  'image', 'cooking_time')


class SubscribedSerializer(serializers.ModelSerializer):
    """Список обьектов на которые подписан юзер."""

    email = serializers.ReadOnlyField()
    username = serializers.ReadOnlyField()
    is_subscribed = serializers.SerializerMethodField()
    recipes = RecipeSerializer(many=True, read_only=True)
    recipes_count = serializers.SerializerMethodField()
    first_name = serializers.ReadOnlyField()
    last_name = serializers.ReadOnlyField()

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
