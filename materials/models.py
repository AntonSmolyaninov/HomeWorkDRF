from django.db import models


class Course(models.Model):
    """
    Модель курса, представляющая образовательную программу.

    Эта модель хранит информацию о курсе, включая его название,
    визуальное представление (превью) и описание содержания.

    Attributes:
        title (CharField): Название курса (обязательное поле)
        preview (ImageField): Превью-изображение курса (опционально)
        description (TextField): Описание курса (опционально)
    """

    title = models.CharField(
        max_length=100, verbose_name="Название", help_text="Укажите название курса"
    )
    preview = models.ImageField(
        upload_to="materials/course",
        blank=True,
        null=True,
        verbose_name="Превью",
        help_text="Загрузите превью",
    )
    description = models.TextField(
        blank=True, null=True, verbose_name="Описание", help_text="Введите описание"
    )
    owner = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Владелец",
        help_text="укажите владельца",
    )

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"

    def __str__(self):
        return self.title


class Lesson(models.Model):
    """
    Модель урока, принадлежащего определенному курсу.

    Эта модель хранит информацию об отдельном уроке в рамках курса,
    включая его название, описание, превью и ссылку на видео.

    Attributes:
        title (CharField): Название урока (обязательное поле)
        preview (ImageField): Превью-изображение урока (опционально)
        description (TextField): Описание урока (опционально)
        video_url (URLField): Ссылка на видео-материал (опционально)
        course (ForeignKey): Ссылка на родительский курс
    """

    title = models.CharField(
        max_length=100, verbose_name="Название", help_text="Укажите название урока"
    )
    preview = models.ImageField(
        upload_to="lesson/course",
        blank=True,
        null=True,
        verbose_name="Превью",
        help_text="Загрузите превью",
    )
    description = models.TextField(
        blank=True, null=True, verbose_name="Описание", help_text="Введите описание"
    )
    video_url = models.URLField(blank=True, null=True, verbose_name="Ссылка на видео")
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="lessons", verbose_name="Курс"
    )
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

    def __str__(self):
        """
        Строковое представление объекта урока.
        """
        return f"{self.title} (Курс: {self.course.title})"
