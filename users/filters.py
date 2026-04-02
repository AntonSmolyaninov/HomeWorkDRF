# users/filters.py
from django_filters import rest_framework as filters

from .models import Payment


class PaymentFilter(filters.FilterSet):
    """
    Фильтр для модели Payment.
    Позволяет фильтровать по курсу, уроку и способу оплаты.
    """

    # Фильтр по курсу (по ID курса)
    course = filters.NumberFilter(field_name="course__id", lookup_expr="exact")
    course__title = filters.CharFilter(
        field_name="course__title", lookup_expr="icontains"
    )

    # Фильтр по уроку (по ID урока)
    lesson = filters.NumberFilter(field_name="lesson__id", lookup_expr="exact")
    lesson__title = filters.CharFilter(
        field_name="lesson__title", lookup_expr="icontains"
    )

    # Фильтр по способу оплаты
    payment_method = filters.ChoiceFilter(
        field_name="payment_method", choices=Payment.PaymentMethod.choices
    )

    # Фильтр по дате (диапазон)
    payment_date_from = filters.DateTimeFilter(
        field_name="payment_date", lookup_expr="gte"
    )
    payment_date_to = filters.DateTimeFilter(
        field_name="payment_date", lookup_expr="lte"
    )

    # Фильтр по пользователю
    user = filters.NumberFilter(field_name="user__id", lookup_expr="exact")
    user__email = filters.CharFilter(field_name="user__email", lookup_expr="icontains")

    # Фильтр по сумме (диапазон)
    amount_min = filters.NumberFilter(field_name="amount", lookup_expr="gte")
    amount_max = filters.NumberFilter(field_name="amount", lookup_expr="lte")

    class Meta:
        model = Payment
        fields = [
            "course",
            "course__title",
            "lesson",
            "lesson__title",
            "payment_method",
            "user",
            "user__email",
            "amount_min",
            "amount_max",
        ]
