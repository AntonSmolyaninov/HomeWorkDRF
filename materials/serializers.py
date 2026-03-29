from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from materials.models import Course, Lesson


class CourseSerializer(ModelSerializer):
    """
    Базовый сериализатор для модели Course.
    Используется для списка курсов и создания/обновления.
    """
    lessons_count = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = "__all__"

    def get_lessons_count(self, obj):
        return obj.lessons.count()


class LessonSerializer(ModelSerializer):
    """
    Сериализатор для модели Lesson.
    Используется для всех операций с уроками.
    """

    class Meta:
        model = Lesson
        fields = "__all__"


class CourseDetailSerializer(ModelSerializer):
    """
    Детальный сериализатор для модели Course.
    Используется для просмотра одного курса с уроками.
    """
    lessons_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = "__all__"
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_lessons_count(self, obj):
        return obj.lessons.count()
