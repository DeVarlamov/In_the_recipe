import re

from rest_framework import serializers


def validate_slug(value):
    """
    Валидация запрета недопустимых символов для слаг
    """
    invalid_chars_regex = re.compile(r'^[-a-zA-Z0-9_]+$')
    invalid_chars = re.findall(invalid_chars_regex, value)
    if invalid_chars:
        raise serializers.ValidationError(
            'Slug содержит недопустимые'
            f'символы: {", ".join(invalid_chars)}',
        )


def validate_color(value):
    """
    Валидация запрета недопустимых символов цвета
    """
    invalid_chars_regex = re.compile(r'^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$')
    invalid_chars = re.findall(invalid_chars_regex, value)
    if invalid_chars:
        raise serializers.ValidationError(
            'Пожауста убедитесь что цвет существует'
            f'ошибка символов: {", ".join(invalid_chars)}',
        )


def validate_not_empty(value):
    """Валидация кооличества < 1"""
    if len(value) < 1:
        raise serializers.ValidationError(
            'Количество не может быть меньше одного')
