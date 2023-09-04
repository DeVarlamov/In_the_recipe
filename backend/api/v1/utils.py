from recipes.models import Recipe
from rest_framework import response, status
from rest_framework.generics import get_object_or_404


def adding_deleting(add_serializer, model, request, recipe_id):
    """Кастомный метод добавления и удаления рецепта."""
    user = request.user
    data = {'user': user.id,
            'recipe': recipe_id}
    serializer = add_serializer(data=data, context={'request': request})
    if request.method == 'POST':
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return response.Response(serializer.data,
                                 status=status.HTTP_201_CREATED)
    get_object_or_404(
        model, user=user, recipe=get_object_or_404(Recipe, id=recipe_id)
    ).delete()
    return response.Response(status=status.HTTP_204_NO_CONTENT)


def create_shopping_cart_file(ingredients):
    """Кастомный метод создания списка."""
    content = 'Список покупок:\n\n'
    for item in ingredients:
        content += (f"{item['ingredient__name']} - {item['total_amount']} "
                    f"{item['ingredient__measurement_unit']}\n")
    return content
