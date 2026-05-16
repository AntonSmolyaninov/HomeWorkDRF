from django.db import models


class Course(models.Model):
    """Модель курса"""

    title = models.CharField(max_length=100, verbose_name="Название", help_text="Укажите название курса")
    preview = models.ImageField(
        upload_to="materials/course",
        blank=True,
        null=True,
        verbose_name="Превью",
        help_text="Загрузите превью",
    )
    description = models.TextField(blank=True, null=True, verbose_name="Описание", help_text="Введите описание")
    owner = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Владелец",
        help_text="укажите владельца",
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
        verbose_name="Цена",
        help_text="Укажите цену курса",
    )
    stripe_product_id = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Stripe Product ID",
        help_text="ID продукта в Stripe",
    )
    last_notification_sent = models.DateTimeField(null=True, blank=True, verbose_name="Последнее уведомление")

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"
        ordering = ['id']  # Добавлено для устранения предупреждений пагинации

    def __str__(self):
        return self.title


class Lesson(models.Model):
    """Модель урока"""

    title = models.CharField(max_length=100, verbose_name="Название", help_text="Укажите название урока")
    preview = models.ImageField(
        upload_to="lesson/course",
        blank=True,
        null=True,
        verbose_name="Превью",
        help_text="Загрузите превью",
    )
    description = models.TextField(blank=True, null=True, verbose_name="Описание", help_text="Введите описание")
    video_url = models.URLField(blank=True, null=True, verbose_name="Ссылка на видео")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="lessons", verbose_name="Курс")
    owner = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Владелец",
        help_text="укажите владельца",
    )

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
        ordering = ['id']  # Добавлено для устранения предупреждений пагинации

    def __str__(self):
        return f"{self.title} (Курс: {self.course.title})"


class Subscription(models.Model):
    """Модель подписки"""

    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="subscriptions",
        verbose_name="Пользователь",
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="subscribers",
        verbose_name="Курс",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата подписки")

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"
        unique_together = ["user", "course"]
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.email} подписан на {self.course.title}"
