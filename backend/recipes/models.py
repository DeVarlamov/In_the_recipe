from colorfield.fields import ColorField
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from foodgram.constants import (
    AMOUNT_MAX,
    AMOUNT_MIN,
    COLOR_ERROR,
    COOKE_TAME_MAX,
    COOKE_TAME_MIN,
    DEFAULT_COLOR,
    DIRICTORY_PATH,
    INGREDIENT_UNITS,
    LENGTH_FOR_COLOR,
    MAXIMUM_COUNT,
    MAXIMUM_LENGTH,
    MAXIMUMTIME,
    MIN_COUNT,
    NAME_ERROR,
    NAME_INGRIDENT_RERROR,
    SLUG_ERROR,
)
from users.models import User


class Tag(models.Model):
    """Модель Тегов."""

    name = models.CharField(
        'Название Тега',
        max_length=MAXIMUM_LENGTH,
        unique=True,
        error_messages={
            'unique': NAME_ERROR,
        },
    )
    color = ColorField(
        'Цвет в HeX',
        max_length=LENGTH_FOR_COLOR,
        unique=True,
        error_messages={
            'unique': COLOR_ERROR,
        },
        default=DEFAULT_COLOR,
        null=True,
    )
    slug = models.SlugField(
        'Уникальный Тег',
        max_length=MAXIMUM_LENGTH,
        unique=True,
        error_messages={
            'unique': SLUG_ERROR,
        },
    )

    class Meta:
        ordering = ('name',)
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """Модель ингредиент"""

    name = models.CharField(
        'Название',
        max_length=MAXIMUM_LENGTH,
        db_index=True,
        error_messages={
            'unique': NAME_INGRIDENT_RERROR,
        },
    )
    measurement_unit = models.CharField(
        'Единица измерения',
        max_length=MAXIMUM_LENGTH,
        choices=INGREDIENT_UNITS,
    )

    class Meta:
        ordering = ['name']
        verbose_name = "ингредиент"
        verbose_name_plural = "ингредиенты"
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'measurement_unit'], name='unique_ingredients'
            )
        ]

    def __str__(self):
        return f'{self.name},в {self.measurement_unit}'


class ImportIngredient(models.Model):
    """Модель импорта ингридиентов."""

    csv_file = models.FileField(upload_to='uploads/')
    date_added = models.DateTimeField(auto_now_add=True)


class Recipe(models.Model):
    """Модель рецептов."""

    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient',
        through_fields=('recipe', 'ingredient'),
        verbose_name='Ингредиенты',
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Теги',
    )
    image = models.ImageField(
        'Изображение блюда',
        upload_to=DIRICTORY_PATH,
    )
    name = models.CharField(
        'Название блюда',
        max_length=MAXIMUM_LENGTH,
    )
    text = models.TextField(
        'Описание',
    )
    cooking_time = models.PositiveSmallIntegerField(
        'Время приготовления, мин',
        default=MIN_COUNT,
        validators=[
            MinValueValidator(MIN_COUNT, message=COOKE_TAME_MIN),
            MaxValueValidator(MAXIMUMTIME, message=COOKE_TAME_MAX),
        ],
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор рецепта',
    )
    pub_date = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата публикации'
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    """Модель связывает Recipe и Ingredient с
    указанием количества ингредиентов.
    """

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Рецепт',
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='ingredients',
        verbose_name='Ингредиенты',
    )
    amount = models.PositiveSmallIntegerField(
        'Количество',
        default=MIN_COUNT,
        validators=[
            MinValueValidator(MIN_COUNT, message=AMOUNT_MIN),
            MaxValueValidator(MAXIMUM_COUNT, message=AMOUNT_MAX),
        ],
    )

    class Meta:
        ordering = ('recipe',)
        verbose_name = 'Ингредиенты в рецепте'
        verbose_name_plural = 'Ингредиенты в рецептах'
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'], name='unique_combination'
            )
        ]

    def __str__(self):
        return f'{self.recipe} содержит ингредиент/ты {self.ingredient}'


class UserRelation(models.Model):
    """Связь подписок"""

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, verbose_name='Рецепт'
    )

    class Meta:
        ordering = ('id',)
        abstract = True
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'], name='unique_%(class)s'
            )
        ]

    def __str__(self):
        return f'{self.user.username} - {self.recipe.id}'


class Favorite(UserRelation):
    """Подписка на избранное"""

    class Meta(UserRelation.Meta):
        default_related_name = 'favorite'
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'


class ShoppingСart(UserRelation):
    """Рецепты в корзине покупок.
    Модель связывает Recipe и User.
    """

    class Meta(UserRelation.Meta):
        default_related_name = 'shoppingcart'
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзина'
