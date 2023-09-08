from djoser.serializers import UserCreateSerializer
from rest_framework import serializers

from .models import User


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
