from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from foodgram.settings import CHARACTER_LENGTH, LENGTH_FOR_MAIL

from users.validate import validate_username


class User(AbstractUser):
    """Абстрактная модель пользователя"""
    username = models.CharField(
        _('Ваш логин'),
        max_length=CHARACTER_LENGTH,
        unique=True,
        help_text=_('введите username'),
        validators=(validate_username,),
        error_messages={
            'unique': _('Пользователь с таким username уже существует.'),
        },
    )
    email = models.EmailField(
        _('Почта'),
        max_length=LENGTH_FOR_MAIL,
        unique=True,
        error_messages={
            'unique': _('e-mail уже занят.'),
        },
    )
    first_name = models.CharField(_('Имя'), max_length=CHARACTER_LENGTH)
    last_name = models.CharField(_('Фамилия'), max_length=CHARACTER_LENGTH)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [
        'username',
        'first_name',
        'last_name',
    ]

    class Meta:
        ordering = ('id',)
        verbose_name = _('Пользователь')
        verbose_name_plural = _('Пользователи')

    def __str__(self):
        return self.username


class Following(models.Model):
    """Модель подписки"""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Подписчик',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='followings',
        verbose_name='Автор',
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        ordering = ['-id']
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique_following')]

    def __str__(self):
        return f'Пользователь {self.user} -> автор {self.author}'
