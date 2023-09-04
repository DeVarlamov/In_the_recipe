from django.forms import ValidationError
from django.shortcuts import get_object_or_404
from drf_extra_fields.fields import Base64ImageField
from foodgram.constants import MAXIMUMCOUNT, MAXIMUMTIME, MINCOUNT
from recipes.models import Ingredient, Recipe, RecipeIngredient, Tag
from rest_framework.serializers import (
    IntegerField,
    ModelSerializer,
    PrimaryKeyRelatedField,
    ReadOnlyField,
    SerializerMethodField,
)
from users.models import User


class UserDateSerializer(ModelSerializer):  # Продублировал код и за ошибки
    """Сереалайзер данных юзера."""         # с цикличностью

    is_subscribed = SerializerMethodField()

    class Meta:
        model = User
        fields = ('email',
                  'id',
                  'username',
                  'first_name',
                  'last_name',
                  'is_subscribed',
                  )

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        return (
            user.is_authenticated
            and obj.subscribing.filter(user=user).exists()
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

    tags = TagSerializer(many=True,
                         read_only=True)
    author = UserDateSerializer()
    ingredients = RecipeIngredientSerializer(
        many=True, read_only=True, source='recipes',
    )
    is_favorited = SerializerMethodField()
    is_in_shopping_cart = SerializerMethodField()
    image = ReadOnlyField(source='image.url')

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
        return bool(request and request.user.is_authenticated and bool(
            obj.user.favorite.filter(recipe=obj, user=request.user).exists()))

    def get_is_in_shopping_cart(self, obj):
        """Проверка - находится ли рецепт в списке покупок."""
        request = self.context.get('request')
        return bool(request and request.user.is_authenticated and bool(
            obj.user.shoppingcart.filter(recipe=obj,
                                         user=request.user).exists()))


class GetIngredientSerilizer(ModelSerializer):
    """Сереалайзер колличества ингридиентов в рецепте."""

    ingredient = PrimaryKeyRelatedField(queryset=Ingredient.objects.all())
    amount = IntegerField(min_value=MINCOUNT, max_value=MAXIMUMCOUNT)

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
    cooking_time = IntegerField(min_value=MINCOUNT, max_value=MAXIMUMTIME)
    ingredients = GetIngredientSerilizer(many=True)
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('id', 'image', 'tags', 'ingredients',
                  'name', 'text', 'cooking_time')

    @staticmethod
    def create_recipe_ingredients(recipe, ingredients_data):
        """
        Вспомогательный метод для обработки
        создания объектов RecipeIngredient.
        """
        RecipeIngredient.objects.filter(recipe=recipe).clear()
        recipe_ingredients = []
        for ingredient_data in ingredients_data:
            ingredient = get_object_or_404(Ingredient,
                                           id=ingredient_data['id'])
            amount = ingredient_data['amount']
            recipe_ingredients.append(
                RecipeIngredient(recipe=recipe, ingredient=ingredient,
                                 amount=amount)
            )
        RecipeIngredient.objects.bulk_create(recipe_ingredients)

    def create(self, validated_data):
        """Создание рецепта."""

        tags_data = validated_data.pop('tags')
        ingredients_data = validated_data.pop('ingredients')
        image = validated_data.get('image')
        if not image:
            raise ValidationError("Поле image не может быть пустым.")
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags_data)
        create_recipe_ingredients(recipe, ingredients_data)
        return recipe

    def update(self, instance, validated_data):
        """Редактирование рецепта."""
        tags_data = validated_data.pop('tags', None)
        instance.tags.set(tags_data)
        ingredients_data = validated_data.pop('ingredients', None)
        create_recipe_ingredients(instance, ingredients_data)
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        return RecipeListSerializer(instance,
                                    context=self.context).data
