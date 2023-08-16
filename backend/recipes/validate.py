import re
from django.forms import ValidationError

from rest_framework import serializers


def validate_slug(value):
    """
    Валидация запрета недопустимых символов для слаг
    """
    pattern = r'^[-a-zA-Z0-9_]+$'
    match = re.match(pattern, value)
    if not match:
        raise ValueError('Введите правильное значение.')


def validate_color(value):
    """
    Валидация запрета недопустимых символов цвета
    """
    pattern = r'^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$'
    match = re.match(pattern, value)
    if not match:
        raise ValueError('Введите правильное значение цвета в формате HEX.')


def validate_not_empty(value):
    """Валидация кооличества < 1"""
    if len(value) < 1:
        raise serializers.ValidationError(
            'Количество не может быть меньше одного')


def validate_measurement_unit(value):
    valid_units = ['kg', 'g', 'l', 'ml', 'tsp', 'tbsp', 'cup', 'oz', 'lb',
                   'кг', 'г', 'л', 'мл', 'ч.л.',
                   'ст.л.', 'стакан', 'унция', 'фунт', 'шт']
    if value not in valid_units:
        raise ValidationError('Недопустимая единица измерения')
