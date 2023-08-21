from django.contrib import admin

from .models import Favorite, Recipe, RecipeIngredient, Tag, Ingredient, ShoppingСart


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Админка Тегов"""
    model = Tag
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'color', 'slug')
    list_editable = ('color',)
    empty_value_display = '-пусто-'


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    """Админка ингридиентов"""
    model = Ingredient
    list_display = ('pk', 'name', 'measurement_unit')
    list_filter = ('name', )
    search_fields = ('name', 'measurement_unit')


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'cooking_time', 'text', 'image', 'author', )
    list_editable = ('cooking_time', 'text', 'image', 'author')
    list_filter = ('name', 'author', 'tags')
    empty_value_display = '-пусто-'


@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'recipe', 'ingredient', 'amount')
    list_editable = ('recipe', 'ingredient', 'amount')


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'recipe')
    list_editable = ('user', 'recipe')


@admin.register(ShoppingСart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'recipe')
    list_editable = ('user', 'recipe')
