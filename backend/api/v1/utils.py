from recipes.models import Ingredient, RecipeIngredient


def create_recipe_ingredients(recipe, ingredients_data):
    """
    Вспомогательный метод для обработки
    создания объектов RecipeIngredient.
    """
    RecipeIngredient.objects.filter(recipe=recipe).delete()
    for ingredient_data in ingredients_data:
        ingredient = Ingredient.objects.get(pk=ingredient_data['id'])
        amount = ingredient_data['amount']
        RecipeIngredient.objects.create(
            recipe=recipe,
            ingredient=ingredient,
            amount=amount
        )
