# materials/tasks.py
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from datetime import timedelta


@shared_task
def send_course_update_notification(course_id, user_emails, course_title):
    """Отправка уведомлений об обновлении курса подписчикам"""

    if not user_emails:
        return f"Нет подписчиков для курса '{course_title}'"

    subject = f"Курс '{course_title}' был обновлен!"
    message = f"""
    Здравствуйте!

    Курс "{course_title}" был обновлен. Добавлены новые материалы или изменения.

    Приглашаем вас ознакомиться с обновлениями.

    С уважением,
    Команда платформы
    """

    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=user_emails,
            fail_silently=False,
        )
        return f"Уведомления отправлены {len(user_emails)} подписчикам курса '{course_title}'"
    except Exception as e:
        return f"Ошибка при отправке: {str(e)}"


@shared_task
def send_lesson_update_notification(lesson_id, course_id, user_emails, lesson_title):
    """Отправка уведомлений об обновлении урока подписчикам курса"""

    if not user_emails:
        return f"Нет подписчиков для урока '{lesson_title}'"

    subject = f"Урок '{lesson_title}' в вашем курсе был обновлен!"
    message = f"""
    Здравствуйте!

    Урок "{lesson_title}" в одном из ваших курсов был обновлен. Добавлены новые материалы или изменения.

    Приглашаем вас ознакомиться с обновлениями.

    С уважением,
    Команда платформы
    """

    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=user_emails,
            fail_silently=False,
        )
        return f"Уведомления отправлены {len(user_emails)} подписчикам об обновлении урока '{lesson_title}'"
    except Exception as e:
        return f"Ошибка при отправке: {str(e)}"


@shared_task
def check_course_update_and_notify(course_id, updated_fields):
    """Проверяет, нужно ли отправлять уведомление об обновлении курса"""
    from materials.models import Course, Subscription
    from users.models import User

    try:
        course = Course.objects.get(id=course_id)

        # Дополнительное задание: проверка на 4 часа
        if course.last_notification_sent:
            time_since_last = timezone.now() - course.last_notification_sent
            if time_since_last < timedelta(hours=4):
                return f"Уведомление не отправлено. Последнее уведомление было {time_since_last.total_seconds() / 3600:.1f} часов назад"

        # Получаем подписчиков курса
        subscribers = Subscription.objects.filter(course=course).select_related('user')
        subscriber_emails = [sub.user.email for sub in subscribers if sub.user.email]

        if subscriber_emails:
            # Отправляем уведомление
            send_course_update_notification.delay(course_id, subscriber_emails, course.title)

            # Обновляем время последнего уведомления
            course.last_notification_sent = timezone.now()
            course.save(update_fields=['last_notification_sent'])

            return f"Уведомление отправлено {len(subscriber_emails)} подписчикам"

        return "Нет подписчиков для уведомления"

    except Course.DoesNotExist:
        return f"Курс с ID {course_id} не найден"
