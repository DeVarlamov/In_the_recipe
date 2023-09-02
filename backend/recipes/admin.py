import csv

from django.contrib import admin, messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import path, reverse

from .forms import IngredientImportForm
from .models import (
    Favorite,
    ImportIngredient,
    Ingredient,
    Recipe,
    RecipeIngredient,
    ShoppingСart,
    Tag,
)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Админка Тегов"""
    model = Tag
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'color', 'slug')
    list_editable = ('color',)
    empty_value_display = '-пусто-'


@admin.register(ImportIngredient)
class ImportIngredient(admin.ModelAdmin):
    list_display = ('csv_file', 'date_added')


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    """Админка ингридиентов и импорт-CSV"""
    model = Ingredient
    list_display = ('pk', 'name', 'measurement_unit')
    search_fields = ('name', 'measurement_unit')

    def get_urls(self):
        urls = super().get_urls()
        urls.insert(-1, path('csv-upload/', self.upload_csv))
        return urls

    def upload_csv(self, request):
        if request.method == 'POST':
            form = IngredientImportForm(request.POST, request.FILES)
            if form.is_valid():
                form_object = form.save()
                with open(form_object.csv_file.path,
                          encoding='utf-8') as csv_file:
                    rows = csv.reader(csv_file, delimiter=',')
                    if next(rows) != ['name', 'measurement_unit']:
                        messages.warning(request, 'Неверные заголовки у файла')
                        return HttpResponseRedirect(request.path_info)
                    Ingredient.objects.bulk_create(
                        Ingredient(name=row[0],
                                   measurement_unit=row[1],
                                   )
                        for row in rows)
                url = reverse('admin:index')
                messages.success(request, 'Файл успешно импортирован')
                return HttpResponseRedirect(url)
        form = IngredientImportForm()
        return render(request, 'admin/csv_import_page.html', {'form': form})


class IngredientInRecipeInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 2
    min_num = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'pub_date', 'name', 'text', 'cooking_time',
                    'get_tags', 'get_ingredients', 'count_favorites',)
    readonly_fields = ('count_favorites',)
    list_filter = ('name', 'tags',)
    search_fields = (
        'name', 'cooking_time',
        'author__email', 'ingredient__name')
    empty_value_display = '-пусто-'
    inlines = (IngredientInRecipeInline,)

    @admin.display(description='Количество в избранных')
    def count_favorites(self, obj):
        """Получаем количество избранных."""
        return obj.favorites.count()

    @admin.display(description='Ингредиенты')
    def get_ingredients(self, obj):
        """Получаем ингредиенты."""
        return '\n '.join([
            f'{item["ingredient__name"]} - {item["amount"]}'
            f' {item["ingredient__measurement_unit"]}.'
            for item in obj.ingredient_list.values(
                'ingredient__name',
                'amount', 'ingredient__measurement_unit')])

    @admin.display(description='Тэги')
    def get_tags(self, obj):
        """Получаем теги."""
        return ', '.join(_.name for _ in obj.tags.all())


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
