from rest_framework import serializers
from recipes.models import Recipes, Tags, Ingredients
from drf_extra_fields.fields import Base64ImageField

class TagsSerializer(serializers.ModelSerializer):
    """Сереалайзер Тега"""
    class Meta:
        model = Tags
        fields = '__all__'


class IngredientsSerializer(serializers.ModelSerializer):
    """Сереолайзер ингридиента"""
    class Meta:
        model = Ingredients
        fields = '__all__'

class RecipesSerializer(serializers.ModelSerializer):
    """Сереолайзер Рецепта"""
    image = Base64ImageField()

    class Meta:
        model = Recipes
        fields = ('id', 'name', 'image', 'cooking_time')

class Favorite_recipesSerializer(serializers.ModelSerializer):
    
