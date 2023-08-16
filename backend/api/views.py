from rest_framework import filters
from recipes.models import Ingredient, Tag
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ReadOnlyModelViewSet

from api.serializers import IngredientSerializer, TagSerializer


class TagViewSet(ReadOnlyModelViewSet):
    """Вьюсет тегов"""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AllowAny,)


class IngredientViewSet(ReadOnlyModelViewSet):
    """Вьюсет ингридеентов"""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (AllowAny,)
    filter_backends = (filters.SearchFilter, )
    search_fields = ('^name', 'name')
