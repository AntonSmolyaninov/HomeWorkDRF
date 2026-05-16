from rest_framework import status
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    get_object_or_404,
)
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from materials.models import Course, Lesson, Subscription
from materials.paginators import CoursePagination, LessonPagination
from materials.serializers import CourseSerializer, LessonSerializer, SubscriptionSerializer
from materials.tasks import check_course_update_and_notify  # Добавьте импорт
from services.stripe_service import create_checkout_session
from users.permissions import IsModer, IsOwner


class CourseViewSet(ModelViewSet):
    """
    ViewSet для управления курсами.
    Выводит количество уроков и все уроки курса.
    """

    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = CoursePagination

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        # Получаем старые данные для сравнения
        old_course = self.get_object()

        # Сохраняем обновления
        updated_course = serializer.save(owner=self.request.user)

        # Проверяем, были ли изменения в важных полях
        important_fields = ["title", "description", "price"]
        updated_fields = []

        for field in important_fields:
            if getattr(old_course, field) != getattr(updated_course, field):
                updated_fields.append(field)

        # Если были изменения, отправляем уведомление
        if updated_fields:
            check_course_update_and_notify.delay(updated_course.id, updated_fields)

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = (~IsModer,)
        elif self.action == ["update", "retrieve"]:
            self.permission_classes = (IsModer | IsOwner,)
        elif self.action == ["destroy"]:
            self.permission_classes = (~IsModer | IsOwner,)
        return super().get_permissions()


class LessonCreateAPIView(CreateAPIView):
    """Создание урока"""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsModer, IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonListAPIView(ListAPIView):
    """Список уроков"""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = LessonPagination


class LessonRetrieveAPIView(RetrieveAPIView):
    """Детальная информация об уроке"""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModer | IsOwner]


class LessonUpdateAPIView(UpdateAPIView):
    """Обновление урока"""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModer | IsOwner]

    def perform_update(self, serializer):
        # Получаем старые данные для сравнения
        old_lesson = self.get_object()

        # Сохраняем обновления
        updated_lesson = serializer.save(owner=self.request.user)

        # Проверяем, были ли изменения в важных полях
        important_fields = ["title", "description", "video_url"]
        updated_fields = []

        for field in important_fields:
            if getattr(old_lesson, field) != getattr(updated_lesson, field):
                updated_fields.append(field)

        # Если были изменения, отправляем уведомление для курса
        if updated_fields:
            check_course_update_and_notify.delay(updated_lesson.course.id, updated_fields)


class LessonDestroyAPIView(DestroyAPIView):
    """Удаление урока"""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsOwner | ~IsModer]

    def perform_destroy(self, instance):
        instance.delete()


class SubscriptionAPIView(APIView):
    """
    APIView для управления подпиской пользователя на курс.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # Получаем пользователя из запроса
        user = request.user

        # Получаем id курса из данных запроса
        course_id = request.data.get("course_id")

        if not course_id:
            return Response(
                {"error": "Необходимо указать course_id"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Получаем объект курса
        course_item = get_object_or_404(Course, id=course_id)

        # Получаем объекты подписок по текущему пользователю и курсу
        subs_item = Subscription.objects.filter(user=user, course=course_item)

        # Если подписка у пользователя на этот курс есть - удаляем ее
        if subs_item.exists():
            subs_item.delete()
            message = "подписка удалена"
            status_code = status.HTTP_200_OK
        # Если подписки у пользователя на этот курс нет - создаем ее
        else:
            Subscription.objects.create(user=user, course=course_item)
            message = "подписка добавлена"
            status_code = status.HTTP_201_CREATED

        # Возвращаем ответ в API
        return Response({"message": message}, status=status_code)

    def get(self, request, *args, **kwargs):
        """
        Получение списка подписок текущего пользователя.
        """
        subscriptions = Subscription.objects.filter(user=request.user)
        serializer = SubscriptionSerializer(subscriptions, many=True)
        return Response(serializer.data)


class UserSubscriptionsView(APIView):
    """
    Получение всех курсов, на которые подписан пользователь.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        subscriptions = Subscription.objects.filter(user=request.user).select_related("course")
        courses = [sub.course for sub in subscriptions]
        serializer = CourseSerializer(courses, many=True, context={"request": request})
        return Response(serializer.data)


class CreateCheckoutSessionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, course_id):
        course = Course.objects.get(id=course_id)
        checkout_session = create_checkout_session(course, request.user, request)
        return Response({"checkout_url": checkout_session.url})
