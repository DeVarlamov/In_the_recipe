from api.v1.utils import create_recipe_ingredients
from drf_extra_fields.fields import Base64ImageField
from recipes.models import (
    Favorite,
    Ingredient,
    Recipe,
    RecipeIngredient,
    ShoppingСart,
    Tag,
)
from rest_framework.serializers import (
    IntegerField,
    ModelSerializer,
    PrimaryKeyRelatedField,
    ReadOnlyField,
    SerializerMethodField,
    StringRelatedField,
    ValidationError,
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
    author = StringRelatedField()
    ingredients = RecipeIngredientSerializer(
        many=True, read_only=True, source='recipes',
    )
    is_favorited = SerializerMethodField()
    is_in_shopping_cart = SerializerMethodField()
    image = ReadOnlyField(source='/media/recipe_img/image.url')

    class Meta:
        model = Recipe
        fields = ('id', 'tags',
                  'author', 'ingredients',
                  'is_favorited', 'is_in_shopping_cart',
                  'name', 'image',
                  'text', 'cooking_time')

    def get_is_favorited(self, obj):
        """Проверка - находится ли рецепт в избранном."""
        request = self.context['request']
        return bool(
            request.user.is_authenticated
            and Favorite.objects.filter(user=request.user, recipe=obj).exists()
        )

    def get_is_in_shopping_cart(self, obj):
        """Проверка - находится ли рецепт в списке покупок."""

        return (
            self.context.get('request').user.is_authenticated
            and ShoppingСart.objects.filter(
                user=self.context['request'].user,
                recipe=obj).exists()
        )


class GetIngredientSerilizer(ModelSerializer):
    """Сереалайзер колличества ингридиентов в рецепте."""

    id = IntegerField()
    amount = IntegerField()

    class Meta:
        model = Ingredient
        fields = (
            'id',
            'amount'
        )

    def validate(self, attrs):
        """Валидарнать на количество"""
        if attrs['amount'] < 1:
            raise ValidationError(
                'Количество ингредиента не может быть меньше 1')
        return attrs


class RecipeCreateSerializer(ModelSerializer):
    """Сереолайзер создания, удаления, редактирования рецепта."""

    id = ReadOnlyField()
    tags = PrimaryKeyRelatedField(many=True,
                                  queryset=Tag.objects.all())
    ingredients = GetIngredientSerilizer(many=True)
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('id', 'image', 'tags', 'ingredients',
                  'name', 'text', 'cooking_time')

    def validate_ingredients(self, ingredients):
        """Ингридиентов количества , есть ли они в списке БД"""

        for ingredient in ingredients:
            if not ingredient.get('id'):
                raise ValidationError('Не указан идентификатор ингредиента')
            if not Ingredient.objects.filter(id=ingredient['id']).exists():
                raise ValidationError(
                    f'Ингредиент с id={ingredient["id"]} не найден')
        return ingredients

    def validate(self, obj):
        """Проверка на обезательные поля: name, text,  и cooking_time."""

        for field in ['name', 'text', 'cooking_time']:
            if not obj.get(field):
                raise ValidationError(
                    f'{field}  обезательное к заполнению поле',
                )
        if not obj.get('ingredients'):
            raise ValidationError(
                'Список ингридиентов пуст',
            )

        if not obj.get('tags'):
            raise ValidationError(
                'Тег обезателен',
            )
        inrgedient_id_list = [item['id'] for item in obj.get('ingredients')]
        unique_ingredient_id_list = set(inrgedient_id_list)
        if len(inrgedient_id_list) != len(unique_ingredient_id_list):
            raise ValidationError(
                'Ингредиенты должны быть уникальны.',
            )
        return obj

    def create(self, validated_data):
        """Создание рецепта."""

        tags_data = validated_data.pop('tags')
        ingredients_data = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags_data)
        create_recipe_ingredients(recipe, ingredients_data)
        return recipe

    def update(self, instance, validated_data):
        """Редактирование рецепта."""

        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get(
            'cooking_time', instance.cooking_time)
        tags_data = validated_data.get('tags')
        if tags_data:
            instance.tags.set(tags_data)
        ingredients_data = validated_data.get('ingredients')
        if ingredients_data:
            create_recipe_ingredients(instance, ingredients_data)
        return instance

    def to_representation(self, instance):
        return RecipeListSerializer(instance,
                                    context=self.context).data
