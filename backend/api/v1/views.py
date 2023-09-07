from datetime import datetime as dt
from urllib import response

from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django_filters.rest_framework import DjangoFilterBackend
from requests import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from api.v1.filters import IngredientFilter, RecipeFilter
from foodgram.constants import FILE_NAME
from recipes.models import (
    Favorite,
    Ingredient,
    Recipe,
    RecipeIngredient,
    ShoppingСart,
    Tag,
)

from .permission import IsAuthorOrReadOnly
from .serializers import (
    FavoriteSerializer,
    IngredientSerializer,
    RecipeCreateSerializer,
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
    permission_classes = (IsAuthorOrReadOnly,)
    pagination_class = LimitOffsetPagination
    pagination_class.default_limit = 3
    filter_backends = [DjangoFilterBackend]
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        """Метод определения сереолайзера"""

        if self.action in ('list', 'retrieve'):
            return RecipeListSerializer
        else:
            return RecipeCreateSerializer

    @staticmethod
    def adding_recipe(add_serializer, model, request, recipe_id):
        """Кастомный метод добавления рецепта."""
        user = request.user
        data = {'user': user.id, 'recipe': recipe_id}
        serializer = add_serializer(data=data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return response.Response(
            serializer.data, status=status.HTTP_201_CREATED
        )

    @staticmethod
    def create_shopping_cart_file(self, request, ingredients):
        """Кастомный метод создания списка. покупок"""
        user = self.request.user
        filename = f'{user.username}_{FILE_NAME}'
        today = dt.today()
        shopping_list = (
            f'Список покупок для пользователя: {user.username}\n\n'
            f'Дата: {today:%Y-%m-%d}\n\n'
        )
        shopping_list += '\n'.join(
            [
                f'- {ingredient["ingredient__name"]} '
                f'({ingredient["ingredient__measurement_unit"]})'
                f' - {ingredient["amount"]}'
                for ingredient in ingredients
            ]
        )
        shopping_list += f'\n\nFoodgram ({today:%Y})'
        response = HttpResponse(
            shopping_list, content_type='text.txt; charset=utf-8'
        )
        response['Content-Disposition'] = f'attachment; filename={filename}'
        return response

    @action(
        detail=True, methods=['post'], permission_classes=(IsAuthenticated,)
    )
    def favorite(self, request, pk):
        """Метод создания избраного"""
        return self.adding_recipe(FavoriteSerializer, Favorite, request, pk)

    @favorite.mapping.delete
    def remove_from_favorite(self, request, pk):
        """Метод удаления избраного"""
        get_object_or_404(Favorite, user=request.user, recipe=pk).delete
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True,
        methods=['post'],
        permission_classes=(IsAuthenticated,),
        pagination_class=None,
    )
    def shopping_cart(self, request, pk):
        """Метод добавления рецепта в корзину"""
        return self.adding_recipe(
            ShoppingСartSerializer, ShoppingСart, request, pk
        )

    @shopping_cart.mapping.delete
    def remove_from_shopping_cart(self, request, pk):
        """Метод удаления из корзины"""
        get_object_or_404(ShoppingСart, user=request.user, recipe=pk).delete
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False, methods=['get'], permission_classes=(IsAuthenticated,)
    )
    def download_shopping_cart(self, request):
        """Метод получения списка покупок"""
        ingredients = (
            RecipeIngredient.objects.filter(
                recipe__shoppingcart__user=self.request.user
            )
            .values('ingredient__name', 'ingredient__measurement_unit')
            .order_by('ingredient__name')
            .annotate(amount=Sum('amount'))
        )
        return self.create_shopping_cart_file(self, request, ingredients)
