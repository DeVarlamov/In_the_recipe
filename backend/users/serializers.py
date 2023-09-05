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
