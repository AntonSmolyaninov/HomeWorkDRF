from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Кастомная модель пользователя с авторизацией по email.

    Вместо стандартного username для входа используется email.
    Добавлены дополнительные поля: телефон, город и аватар.
    """

    username = None  # Отключаем поле username

    email = models.EmailField(
        unique=True, verbose_name="почта", help_text="Укажите почту"
    )
    """Email пользователя (используется для входа)"""

    phone = models.CharField(
        max_length=35,
        blank=True,
        null=True,
        verbose_name="Телефон",
        help_text="Укажите телефон",
    )
    """Номер телефона пользователя (необязательно)"""

    city = models.TextField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="Город",
        help_text="Укажите город",
    )
    """Город проживания пользователя (необязательно)"""

    avatar = models.ImageField(
        upload_to="users/avatars",
        blank=True,
        null=True,
        verbose_name="Аватар",
        help_text="Загрузите аватар",
    )
    """Аватар пользователя (необязательно)"""

    USERNAME_FIELD = "email"  # Поле для авторизации
    REQUIRED_FIELDS = []  # Обязательные поля (кроме email и password)

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
