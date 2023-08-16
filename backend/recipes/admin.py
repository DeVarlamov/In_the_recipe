from django.contrib import admin

from .models import Tag, Ingredient


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
