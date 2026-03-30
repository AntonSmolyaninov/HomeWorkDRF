from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from materials.models import Course, Lesson
from materials.serializers import CourseSerializer, LessonSerializer


class CourseViewSet(ModelViewSet):
    """
    ViewSet для управления курсами.
    Выводит количество уроков и все уроки курса.
    """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer  # Используем CourseSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        serializer.save(owner=self.request.user)


class LessonCreateAPIView(CreateAPIView):
    """Создание урока"""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonListAPIView(ListAPIView):
    """Список уроков"""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class LessonRetrieveAPIView(RetrieveAPIView):
    """Детальная информация об уроке"""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class LessonUpdateAPIView(UpdateAPIView):
    """Обновление урока"""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_update(self, serializer):
        serializer.save(owner=self.request.user)


class LessonDestroyAPIView(DestroyAPIView):
    """Удаление урока"""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
