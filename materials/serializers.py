from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from materials.models import Course, Lesson
from materials.validators import validate_forbidden_domains


class LessonSerializer(ModelSerializer):
    """
    Сериализатор для модели Lesson с валидацией YouTube ссылок.
    """

    video_url = serializers.URLField(
        required=False,
        allow_blank=True,
        validators=[validate_forbidden_domains]
    )

    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(ModelSerializer):
    """
    Сериализатор для модели Course.
    Выводит количество уроков и все уроки курса.
    """

    lessons_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = "__all__"

    def get_lessons_count(self, obj):
        """
        Возвращает количество уроков в курсе.
        """
        return obj.lessons.count()
