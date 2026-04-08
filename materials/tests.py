from django.contrib.auth.models import Group
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from materials.models import Course, Lesson, Subscription
from users.models import User


class CourseAPITestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="admin@sky.pro")
        self.course = Course.objects.create(title="Курс тест 1", owner=self.user)
        self.lesson = Lesson.objects.create(
            title="Урок", description="Тестовый урок", course=self.course
        )
        self.client.force_authenticate(user=self.user)

    def test_course_retrieval(self):
        url = reverse("materials:course-detail", args=(self.course.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("title"), self.course.title)

    def test_course_create(self):
        url = reverse("materials:course-list")
        data = {"title": "Курс тест2"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Course.objects.all().count(), 2)

    def test_course_update(self):
        url = reverse("materials:course-detail", args=(self.course.pk,))
        data = {"title": "Курс тест2"}
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("title"), "Курс тест2")

    def test_course_delete(self):
        url = reverse("materials:course-detail", args=(self.course.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Course.objects.all().count(), 0)

    def test_course_list(self):
        url = reverse("materials:course-list")
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.course.pk,
                    "lessons_count": 1,
                    "lessons": [
                        {
                            "id": self.lesson.pk,
                            "video_url": self.lesson.video_url,
                            "title": self.lesson.title,
                            "preview": None,
                            "description": self.lesson.description,
                            "course": self.course.pk,
                            "owner": None,
                        }
                    ],
                    "title": self.course.title,
                    "preview": None,
                    "description": self.course.description,
                    "owner": self.user.pk,
                }
            ],
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)


class LessonAPITestCase(APITestCase):

    def setUp(self):
        moders_group, created = Group.objects.get_or_create(name="moders")
        self.user = User.objects.create(email="admin@sky.pro", is_superuser=True)
        self.user.groups.add(moders_group)
        self.course = Course.objects.create(title="Курс тест 1", owner=self.user)
        self.lesson = Lesson.objects.create(
            title="Урок",
            description="Тестовый урок",
            course=self.course,
            owner=self.user,
        )
        self.client.force_authenticate(user=self.user)

    def test_lesson_retrieval(self):
        url = reverse("materials:lesson-detail", args=(self.lesson.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("title"), self.lesson.title)

    def test_lesson_create(self):
        url = reverse("materials:lesson-create")
        data = {
            "title": "Урок тест 1",
            "description": "Описание урока",
            "course": self.course.pk,
            "owner": self.user.pk,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.all().count(), 2)

    def test_lesson_update(self):
        url = reverse("materials:lesson-update", args=(self.lesson.pk,))
        data = {"title": "Урок тест2"}
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("title"), "Урок тест2")

    def test_lesson_delete(self):
        url = reverse("materials:lesson-delete", args=(self.lesson.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.all().count(), 0)

    def test_lesson_list(self):
        url = reverse("materials:lesson-list")
        response = self.client.get(url)
        data = response.json()
        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.lesson.pk,
                    "title": self.lesson.title,
                    "description": self.lesson.description,
                    "video_url": self.lesson.video_url,
                    "preview": None,
                    "course": self.course.pk,
                    "owner": self.user.pk,
                }
            ],
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)


class SubscriptionAPITestCase(APITestCase):

    def setUp(self):
        # Создаем пользователя и добавляем в группу модераторов
        moderators_group, created = Group.objects.get_or_create(name="moderators")

        self.user = User.objects.create(email="user@sky.pro", is_superuser=False)
        self.user.groups.add(moderators_group)

        # Создаем другого пользователя
        self.other_user = User.objects.create(email="other@sky.pro", is_superuser=False)

        # Создаем курс
        self.course = Course.objects.create(
            title="Тестовый курс", description="Описание курса", owner=self.user
        )

        self.client.force_authenticate(user=self.user)

    def test_subscribe_to_course(self):
        """Тест подписки на курс"""
        url = reverse("materials:subscription")
        data = {"course_id": self.course.pk}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["message"], "подписка добавлена")

        # Проверяем, что подписка создалась
        self.assertTrue(
            Subscription.objects.filter(user=self.user, course=self.course).exists()
        )

    class SubscriptionAPITestCase(APITestCase):

        def setUp(self):
            from django.contrib.auth.models import Group

            moderators_group, created = Group.objects.get_or_create(name="moderators")

            self.user = User.objects.create(email="user@sky.pro")
            self.user.groups.add(moderators_group)

            self.course = Course.objects.create(title="Тестовый курс", owner=self.user)

            self.client.force_authenticate(user=self.user)

        def test_subscribe_to_course(self):
            """Тест подписки на курс"""
            url = reverse("materials:subscription")
            data = {"course_id": self.course.pk}

            response = self.client.post(url, data)

            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertEqual(response.data["message"], "Подписка оформлена")
            self.assertTrue(
                Subscription.objects.filter(user=self.user, course=self.course).exists()
            )

        def test_unsubscribe_from_course(self):
            """Тест отписки от курса"""
            url = reverse("materials:subscription")
            data = {"course_id": self.course.pk}

            # Подписываемся
            self.client.post(url, data)

            # Отписываемся (повторный POST)
            response = self.client.post(url, data)

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data["message"], "Подписка отменена")
            self.assertFalse(
                Subscription.objects.filter(user=self.user, course=self.course).exists()
            )
