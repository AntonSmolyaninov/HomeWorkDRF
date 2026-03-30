from django.db import models
from rest_framework import serializers
from .models import User, Payment
from materials.serializers import CourseSerializer, LessonSerializer


class PaymentSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Payment.
    Выводит дополнительную информацию о пользователе, курсе и уроке.
    """
    user_email = serializers.CharField(source='user.email', read_only=True)
    user_full_name = serializers.SerializerMethodField()
    course_title = serializers.CharField(source='course.title', read_only=True)
    lesson_title = serializers.CharField(source='lesson.title', read_only=True)
    payment_method_display = serializers.CharField(source='get_payment_method_display', read_only=True)

    class Meta:
        model = Payment
        fields = [
            'id', 'user', 'user_email', 'user_full_name',
            'payment_date', 'course', 'course_title',
            'lesson', 'lesson_title', 'amount',
            'payment_method', 'payment_method_display'
        ]
        read_only_fields = ['payment_date']

    def get_user_full_name(self, obj):
        """Возвращает полное имя пользователя"""
        if obj.user.first_name or obj.user.last_name:
            return f"{obj.user.first_name} {obj.user.last_name}".strip()
        return obj.user.email


class UserPaymentSerializer(serializers.ModelSerializer):
    """
    Сериализатор для пользователя с его платежами.
    """
    payments = PaymentSerializer(many=True, read_only=True)
    total_payments = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'phone', 'city', 'payments', 'total_payments']

    def get_total_payments(self, obj):
        """Возвращает общую сумму платежей пользователя"""
        total = obj.payments.aggregate(total=models.Sum('amount'))['total']
        return total if total else 0
