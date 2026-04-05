from django.core.management.base import BaseCommand

from materials.models import Course, Lesson
from users.models import Payment, User


class Command(BaseCommand):
    help = "Создает тестовые платежи для пользователей"

    def handle(self, *args, **options):
        self.stdout.write("Начинаем создание платежей...")

        # Получаем существующие данные
        users = User.objects.all()
        courses = Course.objects.all()
        lessons = Lesson.objects.all()

        # Проверяем наличие необходимых данных
        if not users.exists():
            self.stdout.write(
                self.style.ERROR("Нет пользователей! Создайте сначала пользователей.")
            )
            return

        if not courses.exists() and not lessons.exists():
            self.stdout.write(
                self.style.ERROR(
                    "Нет курсов и уроков! Создайте сначала курсы или уроки."
                )
            )
            return

        # Создаем платежи
        created_count = 0

        # Платеж 1: Пользователь 1 оплатил курс 1
        if users.count() >= 1 and courses.count() >= 1:
            Payment.objects.create(
                user=users[0],
                course=courses[0],
                lesson=None,
                amount=5000.00,
                payment_method="transfer",
            )
            created_count += 1
            self.stdout.write(
                f'Создан платеж: {users[0].email} - оплата курса "{courses[0].title}" - 5000 руб.'
            )

        # Платеж 2: Пользователь 1 оплатил урок 1
        if users.count() >= 1 and lessons.count() >= 1:
            Payment.objects.create(
                user=users[0],
                course=None,
                lesson=lessons[0],
                amount=1500.00,
                payment_method="cash",
            )
            created_count += 1
            self.stdout.write(
                f'Создан платеж: {users[0].email} - оплата урока "{lessons[0].title}" - 1500 руб.'
            )

        # Платеж 3: Пользователь 2 оплатил курс 2
        if users.count() >= 2 and courses.count() >= 2:
            Payment.objects.create(
                user=users[1],
                course=courses[1],
                lesson=None,
                amount=7500.00,
                payment_method="transfer",
            )
            created_count += 1
            self.stdout.write(
                f'Создан платеж: {users[1].email} - оплата курса "{courses[1].title}" - 7500 руб.'
            )

        # Платеж 4: Пользователь 2 оплатил урок 2
        if users.count() >= 2 and lessons.count() >= 2:
            Payment.objects.create(
                user=users[1],
                course=None,
                lesson=lessons[1],
                amount=2000.00,
                payment_method="cash",
            )
            created_count += 1
            self.stdout.write(
                f'Создан платеж: {users[1].email} - оплата урока "{lessons[1].title}" - 2000 руб.'
            )

        # Платеж 5: Пользователь 3 оплатил курс 1
        if users.count() >= 3 and courses.count() >= 1:
            Payment.objects.create(
                user=users[2],
                course=courses[0],
                lesson=None,
                amount=5000.00,
                payment_method="transfer",
            )
            created_count += 1
            self.stdout.write(
                f'Создан платеж: {users[2].email} - оплата курса "{courses[0].title}" - 5000 руб.'
            )

        # Выводим результат
        self.stdout.write(
            self.style.SUCCESS(f"Успешно создано {created_count} платежей!")
        )

        # Показываем статистику
        if Payment.objects.exists():
            total_amount = sum(payment.amount for payment in Payment.objects.all())
            self.stdout.write(f"Общая сумма всех платежей: {total_amount} руб.")
            self.stdout.write(f"Всего платежей в базе: {Payment.objects.count()}")
