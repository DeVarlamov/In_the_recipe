from django import forms
from django.forms import ModelForm, ValidationError
from django.utils.translation import gettext_lazy as _

from .models import ImportIngredient, Recipe


class IngredientImportForm(ModelForm):
    """Форма добавления ингридиентов при импорте."""

    class Meta:
        model = ImportIngredient
        fields = ('csv_file',)


class RecipeAdminForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        tags = cleaned_data.get('tags')
        ingredients = cleaned_data.get('ingredients')
        if tags.count() < 1:
            raise ValidationError(_('Минимальное колличество тегов 1.'))
        if ingredients.count() < 1:
            raise ValidationError(
                _('Минимальное количество ингредиентов 1.'))
