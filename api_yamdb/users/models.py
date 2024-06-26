from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models

from .validators import username_not_me


class User(AbstractUser):
    """Модель для пользователей."""

    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    ROLE_CHOICES = [
        (USER, 'Пользователь'),
        (MODERATOR, 'Модератор'),
        (ADMIN, 'Администратор'),
    ]

    user_validators = [
        UnicodeUsernameValidator(),
        username_not_me
    ]

    username = models.CharField(
        max_length=settings.USERNAME_MAX_LENGTH,
        verbose_name='Логин',
        help_text='Укажите логин',
        unique=True,
        validators=user_validators
    )

    email = models.EmailField(
        verbose_name='E-mail',
        help_text='Укажите e-mail',
        unique=True,
    )

    first_name = models.CharField(
        max_length=settings.USERNAME_MAX_LENGTH,
        verbose_name='Имя',
        help_text='Укажите ваше имя',
        blank=True,
    )

    last_name = models.CharField(
        max_length=settings.USERNAME_MAX_LENGTH,
        verbose_name='Фамилия',
        help_text='Укажите вашу фамилию',
        blank=True,
    )

    bio = models.TextField(
        verbose_name='О себе',
        help_text='Расскажите о себе',
        blank=True,
    )

    role = models.CharField(
        max_length=max(len(role) for role, _ in ROLE_CHOICES),
        verbose_name='Роль',
        help_text='Права доступа',
        choices=ROLE_CHOICES,
        default=USER,
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    @property
    def is_admin(self):
        return self.is_staff or self.role == self.ADMIN or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    def __str__(self):
        return self.username
