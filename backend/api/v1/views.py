from api.v1.filters import IngredientFilter, RecipeFilter
from api.v1.utils import adding_deleting, create_shopping_cart_file
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from foodgram.constants import FILE_NAME
from recipes.models import (
    Favorite,
    Ingredient,
    Recipe,
    RecipeIngredient,
    ShoppingСart,
    Tag,
)
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from .permission import IsAuthorOrReadOnly
from .serializers import (
    FavoriteSerializer,
    IngredientSerializer,
    RecipeCreateSerializer,
    RecipeIngredientSerializer,
    RecipeListSerializer,
    ShoppingСartSerializer,
    TagSerializer,
)


def my_custom_page_not_found_view(request, exception):
    return render(request, '404.html', status=404)


class TagViewSet(ReadOnlyModelViewSet):
    """Вьюсет тегов."""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AllowAny,)
    pagination_class = None


class IngredientViewSet(ReadOnlyModelViewSet):
    """Вьюсет ингридеентов."""

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (AllowAny,)
    pagination_class = None
    filter_backends = [DjangoFilterBackend]
    filterset_class = IngredientFilter


class RecipeViewSet(ModelViewSet):
    """Вью сет для рецептов."""

    queryset = Recipe.objects.all()
    permission_classes = ((IsAuthorOrReadOnly, ))
    filter_backends = [DjangoFilterBackend]
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        """Метод определения сереолайзера"""

        if self.action in ('list', 'retrieve'):
            return RecipeListSerializer
        elif self.action in ('create', 'update', 'partial_update'):
            return RecipeCreateSerializer
        elif self.action == 'destroy':
            return RecipeIngredientSerializer
        return super().get_serializer_class()

    @action(detail=True, methods=['post', 'delete'],
            permission_classes=(IsAuthenticated,))
    def favorite(self, request, pk):
        return adding_deleting(
            FavoriteSerializer, Favorite, request, pk
        )

    @action(detail=True, methods=['post', 'delete'],
            permission_classes=(IsAuthenticated,),
            pagination_class=None)
    def shopping_cart(self, request, pk):
        """Метод добавления рецепта в корзину"""
        return adding_deleting(
            ShoppingСartSerializer, ShoppingСart, request, pk
        )

    @action(detail=False, methods=['get'],
            permission_classes=(IsAuthenticated,))
    def download_shopping_cart(self, request):
        user = request.user
        shopping_cart = ShoppingСart.objects.filter(user=user)
        ingredients = RecipeIngredient.objects.filter(
            recipe__in=shopping_cart.values('recipe')
        ).values(
            'ingredient__name', 'ingredient__measurement_unit'
        ).annotate(
            total_amount=Sum('amount'))

        content = create_shopping_cart_file(ingredients)

        response = HttpResponse(content, content_type='text/plain')
        response['Content-Disposition'] = f'attachment; filename="{FILE_NAME}"'
        return response
