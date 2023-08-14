from djoser.serializers import UserCreateSerializer
from rest_framework import serializers

from .models import Following, User


class UserRegistrationSerializer(UserCreateSerializer):
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
    is_following = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email',
                  'id',
                  'username',
                  'first_name',
                  'last_name',
                  'is_following',
                  )

    def get_is_following(self, obj):
        user = self.context['request'].user
        if user.is_anonymous:
            return False
        return Following.objects.filter(user=user, author=obj).exists()


class FollowSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='author.id')
    email = serializers.ReadOnlyField(source='author.email')
    username = serializers.ReadOnlyField(source='author.username')
    first_name = serializers.ReadOnlyField(source='author.first_name')
    last_name = serializers.ReadOnlyField(source='author.last_name')
    is_following = serializers.SerializerMethodField()

    class Meta:
        model = Following
        fields = ('id', 'email', 'username', 'first_name', 'last_name',
                  'is_following', 'recipes', 'recipes_count')

    def get_is_following(self, obj):
        return Following.objects.filter(
            user=obj.user,
            author=obj.author,
        ).exists()
