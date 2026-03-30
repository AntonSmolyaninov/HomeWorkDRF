# users/views.py
from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import User, Payment
from .serializers import PaymentSerializer, UserPaymentSerializer
from .filters import PaymentFilter


class PaymentViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления платежами.

    Поддерживает:
    - Сортировку по дате оплаты (ordering=-payment_date, ordering=payment_date)
    - Фильтрацию по курсу (course=1)
    - Фильтрацию по уроку (lesson=1)
    - Фильтрацию по способу оплаты (payment_method=cash или payment_method=transfer)
    - Фильтрацию по пользователю (user=1)
    - Фильтрацию по дате (payment_date_from=2024-01-01, payment_date_to=2024-12-31)
    - Фильтрацию по сумме (amount_min=1000, amount_max=5000)

    Примеры запросов:
    GET /api/users/payments/?ordering=-payment_date
    GET /api/users/payments/?course=1
    GET /api/users/payments/?lesson=2
    GET /api/users/payments/?payment_method=cash
    GET /api/users/payments/?course=1&payment_method=transfer
    GET /api/users/payments/?ordering=-payment_date&course=1
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

    GET /api/users/user-payments/ - список пользователей с платежами
    GET /api/users/user-payments/{id}/ - детали пользователя с его платежами
    """
    queryset = User.objects.all()
    serializer_class = UserPaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Администраторы видят всех пользователей, обычные пользователи - только себя"""
        if self.request.user.is_superuser:
            return User.objects.all().prefetch_related('payments')
        return User.objects.filter(id=self.request.user.id).prefetch_related('payments')
