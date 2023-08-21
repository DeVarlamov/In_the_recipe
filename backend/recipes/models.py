from colorfield.fields import ColorField
from django.db import models
from django.utils.translation import gettext_lazy as _
from users.models import User
from foodgram.settings import (INGREDIENT_UNITS,
                               LENGTH_FOR_COLOR,
                               MAXIMUM_LENGTH,
                               MINIMUM_TIME)
from recipes.validate import validate_color, validate_not_empty, validate_slug


class Tag(models.Model):
    """Модель Тегов"""
    name = models.CharField(
        _('Название Тега'),
        max_length=MAXIMUM_LENGTH,
        unique=True,
        error_messages={
            'unique': _('Тег с таким названием уже существует.'),
        },
    )
    color = ColorField(
        _('Цвет в HeX'),
        max_length=LENGTH_FOR_COLOR,
        unique=True,
        error_messages={
            'unique': _('Такой цвет уже существует.'),
         },
        default='#ffd057',
        validators=(validate_color,),
        null=True
    )
    slug = models.CharField(
        _('Уникальный Тег'),
        max_length=MAXIMUM_LENGTH,
        unique=True,
        error_messages={
            'unique': _('Такой Slug уже существует.'),
            },
        validators=(validate_slug,),
    )

    class Meta:
        verbose_name = _("Тег")
        verbose_name_plural = _("Теги")

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """Модель ингредиент"""
    name = models.CharField(
        _('Название'),
        max_length=MAXIMUM_LENGTH,
        db_index=True,
        unique=True,
        error_messages={
            'unique': _('Такой ингредиент уже есть.'),
            },
    )
    measurement_unit = models.CharField(
        _('Единица измерения'),
        max_length=MAXIMUM_LENGTH,
        choices=INGREDIENT_UNITS,
    )

    class Meta:
        ordering = ['name']
        verbose_name = _("ингредиент")
        verbose_name_plural = _("ингредиенты")

    def __str__(self):
        return f'{self.name},в {self.measurement_unit}'


class Recipe(models.Model):
    """Модель рецептов"""
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient',
        through_fields=('recipe', 'ingredient'),
        verbose_name='Ингредиенты'
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Теги'
    )
    image = models.ImageField(
        _('Изображение блюда'),
        upload_to='recipe_img/',
        )
    name = models.CharField(
        _('Название блюда'),
        max_length=MAXIMUM_LENGTH,
    )
    text = models.TextField(
        _('Описание')
    )
    cooking_time = models.IntegerField(
        _('Время приготовления, мин'),
        default=MINIMUM_TIME,
        validators=(validate_not_empty,),
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор рецепта'
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    """ Модель связывает Recipe и Ingredient с
    указанием количества ингредиентов.
    """
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Рецепт'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='ingredients',
        verbose_name='Ингредиенты'
    )
    amount = models.IntegerField(
        'Количество',
        validators=(validate_not_empty,),
    )

    class Meta:
        verbose_name = 'Ингредиенты в рецепте'
        verbose_name_plural = 'Ингредиенты в рецептах'
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='unique_combination'
            )
        ]

    def __str__(self):
        return (f'{self.recipe.name}: '
                f'{self.ingredient.name} - '
                f'{self.amount} '
                f'{self.ingredient.measurement_unit}')


class UserRelation(models.Model):
    """Связь подписок"""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт'
    )

    class Meta:
        abstract = True
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_favorite'
            )
        ]

    def __str__(self):
        return f'{self.user.username} - {self.recipe.name}'


class Favorite(UserRelation):
    """Подписка на избранное"""
    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_favorite'
            )
        ]


class ShoppingСart(UserRelation):
    """Рецепты в корзине покупок.
    Модель связывает Recipe и  User.
    """

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзина'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_shopping_cart'
            )
        ]
