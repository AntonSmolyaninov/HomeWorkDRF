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
        max_length=100,
        verbose_name="Название",
        help_text="Укажите название курса"
    )
    """
    Название курса.

    Args:
        max_length: Максимальная длина - 100 символов
        verbose_name: Отображаемое имя в админке
        help_text: Подсказка при заполнении поля
    """

    preview = models.ImageField(
        upload_to="materials/course",
        blank=True,
        null=True,
        verbose_name="Превью",
        help_text="Загрузите превью",
    )
    """
    Превью-изображение курса.

    Args:
        upload_to: Директория для загрузки файлов ('materials/course')
        blank=True: Поле может быть пустым в формах
        null=True: Поле может быть NULL в базе данных
        verbose_name: Отображаемое имя в админке
        help_text: Подсказка при заполнении
    """

    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Описание",
        help_text="Введите описание"
    )
    """
    Описание курса.

    Args:
        blank=True: Поле может быть пустым в формах
        null=True: Поле может быть NULL в базе данных
        verbose_name: Отображаемое имя в админке
        help_text: Подсказка при заполнении
    """

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"
        """
        Метаданные модели.

        Attributes:
            verbose_name: Имя модели в единственном числе
            verbose_name_plural: Имя модели во множественном числе
        """

    def __str__(self):
        """
        Строковое представление объекта курса.

        Returns:
            str: Название курса
        """
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
        max_length=100,
        verbose_name="Название",
        help_text="Укажите название урока"
    )
    """
    Название урока.

    Args:
        max_length: Максимальная длина - 100 символов
        verbose_name: Отображаемое имя в админке
        help_text: Подсказка при заполнении поля
    """

    preview = models.ImageField(
        upload_to="lesson/course",
        blank=True,
        null=True,
        verbose_name="Превью",
        help_text="Загрузите превью",
    )
    """
    Превью-изображение урока.

    Args:
        upload_to: Директория для загрузки файлов ('lesson/course')
        blank=True: Поле может быть пустым в формах
        null=True: Поле может быть NULL в базе данных
        verbose_name: Отображаемое имя в админке
        help_text: Подсказка при заполнении
    """

    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Описание",
        help_text="Введите описание"
    )
    """
    Описание урока.

    Args:
        blank=True: Поле может быть пустым в формах
        null=True: Поле может быть NULL в базе данных
        verbose_name: Отображаемое имя в админке
        help_text: Подсказка при заполнении
    """

    video_url = models.URLField(
        blank=True,
        null=True,
        verbose_name="Ссылка на видео"
    )
    """
    Ссылка на видео-материал урока.
    Args:
        blank=True: Поле может быть пустым в формах
        null=True: Поле может быть NULL в базе данных
        verbose_name: Отображаемое имя в админке
    """

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="lessons",
        verbose_name="Курс"
    )
    """
    Связь с моделью Course (многие к одному).

    Args:
        Course: Ссылается на модель Course
        on_delete=models.CASCADE: При удалении курса, все его уроки также удаляются
        related_name="lessons": Обратная связь от Course к Lesson (course.lessons)
        verbose_name: Отображаемое имя в админке

    Example:
        # Получить все уроки курса
        course = Course.objects.get(id=1)
        lessons = course.lessons.all()
    """

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
        """
        Метаданные модели.

        Attributes:
            verbose_name: Имя модели в единственном числе
            verbose_name_plural: Имя модели во множественном числе
        """

    def __str__(self):
        """
        Строковое представление объекта урока.

        Returns:
            str: Название урока с указанием родительского курса

        Example:
            >>> lesson = Lesson.objects.get(id=1)
            >>> print(lesson)
            "Переменные и типы данных (Курс: Python для начинающих)"
        """
        return f"{self.title} (Курс: {self.course.title})"


from rest_framework.serializers import ModelSerializer
from materials.models import Course, Lesson


class CourseSerializer(ModelSerializer):
    """
    Сериализатор для модели Course.

    Этот сериализатор преобразует объекты модели Course в формат JSON и обратно.
    Использует все поля модели для сериализации/десериализации.

    Поля для сериализации:
        - id (автоматическое, только для чтения)
        - title (строка, обязательное)
        - preview (изображение, опционально)
        - description (текст, опционально)
    Attributes:
        model (Course): Связываемая модель
        fields (str): "__all__" - включает все поля модели
    """

    class Meta:
        model = Course
        fields = "__all__"
        """
        Метаданные сериализатора.

        Args:
            model: Модель, которую сериализует этот класс
            fields: "__all__" - использовать все поля модели
                Альтернативные варианты:
                - fields = ['id', 'title', 'description']  # только указанные поля
                - exclude = ['preview']  # исключить указанные поля
        """


class LessonSerializer(ModelSerializer):
    """
    Сериализатор для модели Lesson.

    Этот сериализатор преобразует объекты модели Lesson в формат JSON и обратно.
    Использует все поля модели для сериализации/десериализации.

    Поля для сериализации:
        - id (автоматическое, только для чтения)
        - title (строка, обязательное)
        - preview (изображение, опционально)
        - description (текст, опционально)
        - video_url (URL, опционально)
        - course (ForeignKey, ID связанного курса)
    Attributes:
        model (Lesson): Связываемая модель
        fields (str): "__all__" - включает все поля модели
    """

    class Meta:
        model = Lesson
        fields = "__all__"
        """
        Метаданные сериализатора.

        Args:
            model: Модель, которую сериализует этот класс
            fields: "__all__" - использовать все поля модели
        """
