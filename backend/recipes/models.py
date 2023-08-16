from colorfield.fields import ColorField
from django.db import models
from django.utils.translation import gettext_lazy as _
from foodgram.settings import (INGREDIENT_UNITS,
                               LENGTH_FOR_COLOR,
                               MAXIMUM_LENGTH)
from recipes.validate import validate_color, validate_slug


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
