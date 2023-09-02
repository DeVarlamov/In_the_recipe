from django import forms
from django.forms import ModelForm

from .models import ImportIngredient, Recipe


class IngredientImportForm(ModelForm):
    """Форма добавления ингридиентов при импорте."""

    class Meta:
        model = ImportIngredient
        fields = ('csv_file',)


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = '__all__'

    def clean_ingredients(self):
        ingredients = self.cleaned_data.get('ingredients')
        if ingredients.count() < 1:
            raise forms.ValidationError(
                "Требуется по крайней мере один ингредиент.")
        return ingredients
