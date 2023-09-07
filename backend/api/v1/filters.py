from django_filters.rest_framework import FilterSet, filters

from recipes.models import Ingredient, Recipe


class IngredientFilter(FilterSet):
    """Фильтр ингридиентов."""

    name = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Ingredient
        fields = ('name',)


class RecipeFilter(FilterSet):
    tags = filters.AllValuesMultipleFilter(field_name='tags__slug')
    is_favorited = filters.BooleanFilter(method='is_favorited_filter')
    is_in_shopping_cart = filters.BooleanFilter(
        method='is_in_shopping_cart_filter'
    )

    class Meta:
        model = Recipe
        fields = ('tags', 'author')

    def is_favorited_filter(self, queryset, name, value):
        """Фильтр для избранного с проверкой на is_authenticated"""
        user = self.request.user
        if user.is_authenticated:
            if value:
                return queryset.filter(favorite__user=user)
            else:
                return queryset
        else:
            return queryset.none()

    def is_in_shopping_cart_filter(self, queryset, name, value):
        """Фильтр для карзины с проверкой на is_authenticated"""
        user = self.request.user
        if user.is_authenticated:
            if value:
                return queryset.filter(shoppingcart__user=user)
            else:
                return queryset
        else:
            return queryset.none()
