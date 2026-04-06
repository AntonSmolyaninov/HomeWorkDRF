# users/models.py
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

    def __str__(self):
        return self.email


class Payment(models.Model):
    """
    Модель платежа пользователя за курс или урок.
    """

    class PaymentMethod(models.TextChoices):
        """Способы оплаты"""

        CASH = "cash", "Наличные"
        TRANSFER = "transfer", "Перевод на счет"

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="payments",
        verbose_name="Пользователь",
    )

    payment_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата оплаты")

    course = models.ForeignKey(
        'materials.Course',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="payments",
        verbose_name="Оплаченный курс",
    )

    lesson = models.ForeignKey(
        'materials.Lesson',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="payments",
        verbose_name="Оплаченный урок",
    )

    amount = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Сумма оплаты"
    )

    payment_method = models.CharField(
        max_length=20,
        choices=PaymentMethod.choices,
        default=PaymentMethod.TRANSFER,
        verbose_name="Способ оплаты",
    )

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"
        ordering = ["-payment_date"]

    def __str__(self):
        return f"Платеж {self.amount} от {self.user.email}"
