from colorfield.fields import ColorField
from django.core.validators import MinValueValidator
from django.db import models
from foodgram.settings import LENGTH_FOR_COLOR, MAXIMUM_LENGTH
from recipes.validate import validate_color, validate_not_empty, validate_slug
from users.models import User


class Tags (models.Model):
    """Модель Тегов"""

    name = models.CharField(
        'Название',
        max_length=MAXIMUM_LENGTH,
        unique=True,
    )
    color = ColorField(
        'Цвет в HEX ',
        max_length=LENGTH_FOR_COLOR,
        unique=True,
        default='#ffb057',
        validators=(validate_color,),
    )
    slug = models.SlugField(
        'Slug тега',
        max_length=MAXIMUM_LENGTH,
        unique=True,
        validators=(validate_slug,),
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ('name',)

    def __str__(self):
        return self.name


class AbstractTagIngredients(models.Model):
    """Модель тега имени идигриента"""

    name = models.CharField(
        'Название ингредиента',
        unique=True,
        max_length=MAXIMUM_LENGTH,
        help_text='Введите название',
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class Ingredients(AbstractTagIngredients):
    """Модель ингредиентов"""

    measurement_unit = models.CharField(
        'Единица измерения',
        max_length=MAXIMUM_LENGTH,
    )

    class Meta(AbstractTagIngredients.Meta):
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ('name',)
        constraints = [
            models.UniqueConstraint(fields=['name', 'measurement_unit'],
                                    name='unique_ingredient')
        ]


class Recipes(models.Model):
    """Модель рецептов"""

    ingredients = models.ManyToManyField(
        Ingredients,
        verbose_name='Ингредиенты',
    )
    tags = models.ManyToManyField(
        Tags,
        verbose_name='Теги',
        )
    image = models.ImageField(
        'Изображение',
        upload_to='recipe_image/')
    name = models.CharField(
        'Название',
        max_length=MAXIMUM_LENGTH,
        )
    text = models.TextField(
        'Описание',
    )
    cooking_time = models.IntegerField(
        'Время приготовления (в минутах)',
        validators=[MinValueValidator(1,
                                      message='Время приготовления должно'
                                      'быть не меньше 1 минуты.'),
                    ],
    )
    author = models.ForeignKey(User,
                               verbose_name='Автор рецепта',
                               on_delete=models.SET_NULL,
                               null=True,
                               )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
        editable=False,
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        constraints = [
            models.UniqueConstraint(fields=['author', 'name'],
                                    name='unique_author_name'),
        ]

    def __str__(self):
        return self.name


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorite_recipes',
        verbose_name='Автор списка избранного',
    )
    recipe = models.ForeignKey(
        Recipes,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Рецепт из списка избранного',
    )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные'
        abstract = True
        constraints = [
            models.UniqueConstraint(fields=['user', 'recipe'],
                                    name='unique_favorite_recipes'),
        ]

    def __str__(self):
        return f'{self.recipe} в избранном у {self.user}'


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipes,
        on_delete=models.CASCADE,
        related_name='product_list',

    )
    ingredient = models.ForeignKey(
        Ingredients,
        verbose_name='Ингредиент',
        on_delete=models.CASCADE,
        related_name='product_list',
    )
    amount = models.PositiveSmallIntegerField(
        default=1,
        validators=(validate_not_empty,),
        verbose_name='Количество',
    )

    class Meta():
        ordering = ('-id',)
        verbose_name = 'Количество'
        constraints = [
            models.UniqueConstraint(
                fields=['ingredient', 'recipe'],
                name='unique_ingredient_recipe'
            )
        ]

    def __str__(self):
        return (
            f'{self.ingredient.name} ({self.ingredient.measurement_unit})'
            f' - {self.amount}'
        )


class FavoriteRecipe(Favorite):
    """Модель подписки на рецепт"""

    recipe = models.ForeignKey(
        Recipes,
        on_delete=models.CASCADE,
        related_name='recipes_lists',
        verbose_name='Рецепт',
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes_lists',
        verbose_name='Автор рецепта',
    )

    class Meta(Favorite.Meta):
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'
        default_related_name = 'favorites_recipes'
        constraints = (
            models.UniqueConstraint(
                fields=('recipe', 'user',),
                name='unique_user_recipe',
            ),
        )


class ShoppingList(Favorite):
    """Список покупок"""
    recipe = models.ForeignKey(
            Recipes,
            on_delete=models.CASCADE,
            related_name='shopping_lists',
            verbose_name='Рецепт из списка покупок',
        )
    user = models.ForeignKey(
            User,
            on_delete=models.CASCADE,
            related_name='shopping_lists',
            verbose_name='Автор списка покупок',
        )

    class Meta():
        verbose_name = 'Покупка'
        verbose_name_plural = 'Покупки'
        default_related_name = 'shoppings'
        constraints = [
            models.UniqueConstraint(fields=['user', 'recipe'],
                                    name='unique_shopping')
        ]
