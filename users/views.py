from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import User, Payment
from .serializers import PaymentSerializer, UserPaymentSerializer
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
    ordering_fields = ['payment_date', 'amount']
    ordering = ['-payment_date']  # По умолчанию сортировка по дате (новые сверху)

    def get_queryset(self):
        """
        Пользователи видят только свои платежи.
        Администраторы видят все платежи.
        """
        if self.request.user.is_superuser:
            return Payment.objects.all().select_related('user', 'course', 'lesson')
        return Payment.objects.filter(user=self.request.user).select_related('course', 'lesson')


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
            return User.objects.all().prefetch_related('payments')
        return User.objects.filter(id=self.request.user.id).prefetch_related('payments')
