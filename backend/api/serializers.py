from recipes.models import Ingredient, Tag
from rest_framework.serializers import ModelSerializer


class TagSerializer(ModelSerializer):
    """Сереалайзер тегов."""
    class Meta:
        model = Tag
        fields = '__all__'


class IngredientSerializer(ModelSerializer):
    """Сереализатор ингредиентов."""
    class Meta:
        model = Ingredient
        fields = '__all__'
