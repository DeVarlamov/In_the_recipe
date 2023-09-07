from django.contrib.auth.models import AbstractUser
from django.db import models

from foodgram.constants import CHARACTER_LENGTH, EMAIL_ERROR, USERNAME_ERROR
from users.validate import validate_username


class User(AbstractUser):
    """Абстрактная модель пользователя."""

    username = models.CharField(
        'Ваш логин',
        max_length=CHARACTER_LENGTH,
        unique=True,
        error_messages={
            'unique': USERNAME_ERROR,
        },
        help_text='введите username',
        validators=(validate_username,),
    )
    email = models.EmailField(
        'Почта',
        unique=True,
        error_messages={
            'unique': EMAIL_ERROR,
        },
    )
    password = models.CharField('Пароль', max_length=CHARACTER_LENGTH)
    first_name = models.CharField('Имя', max_length=CHARACTER_LENGTH)
    last_name = models.CharField('Фамилия', max_length=CHARACTER_LENGTH)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [
        'username',
        'first_name',
        'last_name',
    ]

    class Meta:
        ordering = ('email',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class Subscribed(models.Model):
    """Модель подписки."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscriber',
        verbose_name='Подписчик',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscribing',
        verbose_name='Автор',
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        ordering = ['-id']
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique_subscribe')]

    def __str__(self):
        return (f'Пользователь  {self.user}'
                f' подписался на автора {self.author}')
