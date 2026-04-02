from rest_framework import viewsets, permissions, filters, generics, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    UpdateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from users.models import User, Payment
from users.serializers import PaymentSerializer, UserPaymentSerializer, UserSerializer
from .filters import PaymentFilter


class PaymentViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления платежами.
    """

    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    # Настройка фильтрации и сортировки
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = PaymentFilter
    ordering_fields = ["payment_date", "amount"]
    ordering = ["-payment_date"]  # По умолчанию сортировка по дате (новые сверху)

    def get_queryset(self):
        """
        Пользователи видят только свои платежи.
        Администраторы видят все платежи.
        """
        if self.request.user.is_superuser:
            return Payment.objects.all().select_related("user", "course", "lesson")
        return Payment.objects.filter(user=self.request.user).select_related(
            "course", "lesson"
        )


class UserPaymentViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet для просмотра пользователей с их платежами.
    """

    queryset = User.objects.all()
    serializer_class = UserPaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Администраторы видят всех пользователей, обычные пользователи - только себя"""
        if self.request.user.is_superuser:
            return User.objects.all().prefetch_related("payments")
        return User.objects.filter(id=self.request.user.id).prefetch_related("payments")


class UserCreateAPIView(CreateAPIView):
    """
    Регистрация нового пользователя.
    Доступно всем (без авторизации).
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]  # Доступно всем

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class UserListAPIView(ListAPIView):
    """
    Список пользователей.
    Требует авторизации (только для админов).
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]  # Только авторизованные

    def get_queryset(self):
        """Только админы видят всех пользователей"""
        if self.request.user.is_superuser:
            return User.objects.all()
        return User.objects.filter(id=self.request.user.id)


class UserRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    """
    Детальная информация, обновление, удаление пользователя.
    Требует авторизации.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]  # Только авторизованные

    def get_queryset(self):
        """Пользователи могут видеть/обновлять только себя"""
        if self.request.user.is_superuser:
            return User.objects.all()
        return User.objects.filter(id=self.request.user.id)

    def delete(self, request, *args, **kwargs):
        """Проверка прав при удалении"""
        instance = self.get_object()
        if request.user.is_superuser or request.user.id == instance.id:
            self.perform_destroy(instance)
            return Response(
                {"message": "Пользователь успешно удален"},
                status=status.HTTP_204_NO_CONTENT,
            )
        return Response(
            {"error": "У вас нет прав для удаления этого пользователя"},
            status=status.HTTP_403_FORBIDDEN,
        )
