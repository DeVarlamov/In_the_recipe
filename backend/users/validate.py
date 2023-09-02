import re

from rest_framework import serializers


def validate_username(value):
    """
    Валидация запрета недопустимых символов
    """
    invalid_chars_regex = re.compile(r'[^\w.@+-]+')
    invalid_chars = re.findall(invalid_chars_regex, value)
    if invalid_chars:
        raise serializers.ValidationError(
            'Имя пользователя содержит недопустимые'
            f'символы: {", ".join(invalid_chars)}',
        )
    return value
