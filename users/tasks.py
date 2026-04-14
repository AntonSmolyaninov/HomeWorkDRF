from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings

User = get_user_model()


@shared_task
def block_inactive_users():
    """
    Блокирует пользователей, которые не заходили более месяца.
    Отправляет уведомление на email перед блокировкой.
    """
    # Вычисляем дату месяц назад
    month_ago = timezone.now() - timedelta(days=30)

    # Находим активных пользователей, которые не заходили более месяца
    inactive_users = User.objects.filter(
        is_active=True,
        last_login__lt=month_ago
    ).exclude(
        is_superuser=True  # Не блокируем суперпользователей
    )

    blocked_count = 0
    for user in inactive_users:
        # Отправляем предупреждение о блокировке
        send_block_notification.delay(user.id)

        # Блокируем пользователя
        user.is_active = False
        user.save(update_fields=['is_active'])
        blocked_count += 1

    return f"Заблокировано {blocked_count} неактивных пользователей"


@shared_task
def send_block_notification(user_id):
    """
    Отправляет уведомление пользователю о блокировке аккаунта.
    """
    try:
        user = User.objects.get(id=user_id)
        subject = "Ваш аккаунт был заблокирован"
        message = f"""
        Здравствуйте, {user.email}!

        Ваш аккаунт был заблокирован из-за отсутствия активности более месяца.

        Для разблокировки обратитесь к администратору или войдите в систему.

        С уважением,
        Команда платформы
        """

        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )
        return f"Уведомление отправлено пользователю {user.email}"
    except User.DoesNotExist:
        return f"Пользователь с ID {user_id} не найден"


@shared_task
def check_user_activity():
    """
    Проверяет активность пользователей и отправляет напоминания за 3 дня до блокировки.
    """
    # Пользователи, которые не заходили 27 дней (за 3 дня до блокировки)
    warning_date = timezone.now() - timedelta(days=27)

    users_to_warn = User.objects.filter(
        is_active=True,
        last_login__lt=warning_date,
        last_login__gte=warning_date - timedelta(days=1)
    ).exclude(is_superuser=True)

    warned_count = 0
    for user in users_to_warn:
        send_warning_notification.delay(user.id)
        warned_count += 1

    return f"Отправлено напоминаний {warned_count} пользователям"


@shared_task
def send_warning_notification(user_id):
    """
    Отправляет предупреждение пользователю о скорой блокировке.
    """
    try:
        user = User.objects.get(id=user_id)
        subject = "Предупреждение о блокировке аккаунта"
        message = f"""
        Здравствуйте, {user.email}!

        Ваш аккаунт будет заблокирован через 3 дня, если вы не войдете в систему.

        Пожалуйста, войдите в аккаунт, чтобы сохранить доступ.

        С уважением,
        Команда платформы
        """

        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )
        return f"Предупреждение отправлено пользователю {user.email}"
    except User.DoesNotExist:
        return f"Пользователь с ID {user_id} не найден"
