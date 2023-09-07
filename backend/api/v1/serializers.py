from django.forms import ValidationError
from drf_extra_fields.fields import Base64ImageField
from rest_framework.serializers import (
    IntegerField,
    ModelSerializer,
    PrimaryKeyRelatedField,
    ReadOnlyField,
    SerializerMethodField,
)
from rest_framework.validators import UniqueTogetherValidator

from foodgram.constants import (
    FAVORITE_RECIPE,
    IDENTICAL_INGREDIENTS,
    IDENTICAL_TAGS,
    IMAGE_IS_NOT,
    MAXIMUM_COUNT,
    MAXIMUMTIME,
    MIN_COUNT,
    NONE_INGREDIENTS,
    NONE_TEGS,
    SHOPING_LIST,
)
from recipes.models import (
    Favorite,
    Ingredient,
    Recipe,
    RecipeIngredient,
    ShoppingСart,
    Tag,
)


class TagSerializer(ModelSerializer):
    """Сереалайзер тегов."""

    class Meta:
        model = Tag
        fields = '__all__'


class IngredientSerializer(ModelSerializer):
    """Сереализатор ингредиентов."""

    class Meta:
        model = Ingredient
        fields = '__all__'


class RecipeSerializer(ModelSerializer):
    """Список рецептов без ингридиентов."""

    image = ReadOnlyField(source='image.url')
    name = ReadOnlyField()
    cooking_time = ReadOnlyField()

    class Meta:
        model = Recipe
        fields = ('id', 'name',
                  'image', 'cooking_time')


class RecipeIngredientSerializer(ModelSerializer):
    """Список ингредиентов с количеством для рецепта."""

    id = ReadOnlyField(source='ingredient.id')
    name = ReadOnlyField(source='ingredient.name')
    measurement_unit = ReadOnlyField(
        source='ingredient.measurement_unit')

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'name',
                  'measurement_unit', 'amount')


class RecipeListSerializer(ModelSerializer):
    """Сереалайзер списка рецептов."""
    from users.serializers import UserSerializer

    tags = TagSerializer(many=True,
                         read_only=True)
    author = UserSerializer()
    ingredients = RecipeIngredientSerializer(
        many=True, read_only=True, source='recipes',
    )
    is_favorited = SerializerMethodField()
    is_in_shopping_cart = SerializerMethodField()
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('id', 'tags',
                  'author', 'ingredients',
                  'is_favorited', 'is_in_shopping_cart',
                  'name', 'image',
                  'text', 'cooking_time')

    def get_is_favorited(self, obj):
        """Проверка - находится ли рецепт в избранном."""
        request = self.context.get('request')
        return bool(request and request.user.is_authenticated and
                    request.user.favorite.filter(recipe=obj,
                                                 user=request.user).exists())

    def get_is_in_shopping_cart(self, obj):
        """Проверка - находится ли рецепт в списке покупок."""
        request = self.context.get('request')
        return bool(
            request and request.user.is_authenticated and
            request.user.shoppingcart.filter(recipe=obj,
                                             user=request.user).exists()
            )


class GetIngredientSerilizer(ModelSerializer):
    """Сереалайзер колличества ингридиентов в рецепте."""

    id = PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all(),
        source='pk'
    )
    amount = IntegerField(min_value=MIN_COUNT, max_value=MAXIMUM_COUNT)

    class Meta:
        model = Ingredient
        fields = (
            'id',
            'amount'
        )


class RecipeCreateSerializer(ModelSerializer):
    """Сереолайзер создания, удаления, редактирования рецепта."""

    tags = PrimaryKeyRelatedField(many=True,
                                  queryset=Tag.objects.all())
    cooking_time = IntegerField(min_value=MIN_COUNT, max_value=MAXIMUMTIME)
    ingredients = GetIngredientSerilizer(many=True)
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('id', 'image', 'tags', 'ingredients',
                  'name', 'text', 'cooking_time')

    def validate(self, data):
        """Метод валидации для создания рецепта"""
        ingredients = data.get('ingredients')
        tags = data.get('tags')
        image = data.get('image')

        if not ingredients:
            raise ValidationError(NONE_INGREDIENTS)

        if not tags:
            raise ValidationError(NONE_TEGS)

        if not image:
            raise ValidationError(IMAGE_IS_NOT)

        ingredient_ids = [ingredient['id'] for ingredient in ingredients]
        if len(set(ingredient_ids)) != len(ingredient_ids):
            raise ValidationError(IDENTICAL_INGREDIENTS)

        tag_ids = [tag.id for tag in tags]
        if len(set(tag_ids)) != len(tag_ids):
            raise ValidationError(IDENTICAL_TAGS)

        return data

    @staticmethod
    def create_recipe_ingredients(recipe, ingredients_data):
        """Вспомогательный метод для обработки
        создания объектов RecipeIngredient.
        """
        recipe.ingredients.clear()
        recipe_ingredients = []
        for ingredient_data in ingredients_data:
            ingredient_id = ingredient_data['id']
            amount = ingredient_data['amount']
            recipe_ingredients.append(
                RecipeIngredient(recipe=recipe, ingredient_id=ingredient_id,
                                 amount=amount))
        RecipeIngredient.objects.bulk_create(recipe_ingredients)

    def create(self, validated_data):
        """Создание рецепта."""

        tags_data = validated_data.pop('tags', None)
        ingredients_data = validated_data.pop('ingredients', None)
        author = self.context.get('request').user
        recipe = Recipe.objects.create(author=author, **validated_data)
        recipe.tags.set(tags_data)
        self.create_recipe_ingredients(recipe, ingredients_data)
        return recipe

    def update(self, instance, validated_data):
        """Редактирование рецепта."""
        tags_data = validated_data.pop('tags', None)
        instance.tags.set(tags_data)
        ingredients_data = validated_data.pop('ingredients', None)
        self.create_recipe_ingredients(instance, ingredients_data)
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        return RecipeListSerializer(instance,
                                    context=self.context).data


class FavoriteSerializer(ModelSerializer):
    """Сереалайзер избранного"""
    class Meta:
        model = Favorite
        fields = ('user', 'recipe')
        validators = [
            UniqueTogetherValidator(
                queryset=Favorite.objects.all(),
                fields=['user', 'recipe'],
                message=FAVORITE_RECIPE
            )
        ]

    def to_representation(self, instance):
        request = self.context.get('request')
        return RecipeSerializer(
            instance.recipe,
            context={'request': request}
        ).data


class ShoppingСartSerializer(ModelSerializer):
    """Сереалайзер добавления в карзину"""
    class Meta:
        model = ShoppingСart
        fields = ('user', 'recipe')
        validators = [
            UniqueTogetherValidator(
                queryset=ShoppingСart.objects.all(),
                fields=['user', 'recipe'],
                message=SHOPING_LIST
            )
        ]

    def to_representation(self, instance):
        request = self.context.get('request')
        return RecipeSerializer(
            instance.recipe,
            context={'request': request}
        ).data
