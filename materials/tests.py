from unittest.mock import patch
from django.contrib.auth.models import Group
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from materials.models import Course, Lesson, Subscription
from users.models import User


class CourseAPITestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="admin@sky.pro", is_superuser=True)
        self.course = Course.objects.create(title="Курс тест 1", owner=self.user, price=1000.00)
        self.lesson = Lesson.objects.create(
            title="Урок",
            description="Тестовый урок",
            course=self.course,
            owner=self.user,
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
        data = {"title": "Курс тест2", "price": 2000.00}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Course.objects.all().count(), 2)

    @patch('materials.views.check_course_update_and_notify.delay')
    def test_course_update(self, mock_celery):
        url = reverse("materials:course-detail", args=(self.course.pk,))
        data = {"title": "Курс тест2"}
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("title"), "Курс тест2")
        mock_celery.assert_called_once()

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
        self.assertEqual(data["count"], 1)
        self.assertEqual(len(data["results"]), 1)
        self.assertEqual(data["results"][0]["title"], self.course.title)


class LessonAPITestCase(APITestCase):

    def setUp(self):
        moders_group, created = Group.objects.get_or_create(name="moders")
        self.user = User.objects.create(email="admin@sky.pro", is_superuser=True)
        self.user.groups.add(moders_group)
        self.course = Course.objects.create(title="Курс тест 1", owner=self.user, price=1000.00)
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
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.all().count(), 2)

    @patch('materials.views.check_course_update_and_notify.delay')
    def test_lesson_update(self, mock_celery):
        url = reverse("materials:lesson-update", args=(self.lesson.pk,))
        data = {"title": "Урок тест2"}
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("title"), "Урок тест2")
        mock_celery.assert_called_once()

    def test_lesson_delete(self):
        url = reverse("materials:lesson-delete", args=(self.lesson.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.all().count(), 0)

    def test_lesson_list(self):
        url = reverse("materials:lesson-list")
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data["count"], 1)
        self.assertEqual(len(data["results"]), 1)
        self.assertEqual(data["results"][0]["title"], self.lesson.title)


class SubscriptionAPITestCase(APITestCase):

    def setUp(self):
        moderators_group, created = Group.objects.get_or_create(name="moderators")
        self.user = User.objects.create(email="user@sky.pro", is_superuser=False)
        self.user.groups.add(moderators_group)
        self.course = Course.objects.create(
            title="Тестовый курс",
            description="Описание курса",
            owner=self.user,
            price=1000.00,
        )
        self.client.force_authenticate(user=self.user)

    def test_subscribe_to_course(self):
        url = reverse("materials:subscription")
        data = {"course_id": self.course.pk}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["message"], "подписка добавлена")
        self.assertTrue(Subscription.objects.filter(user=self.user, course=self.course).exists())

    def test_unsubscribe_from_course(self):
        url = reverse("materials:subscription")
        data = {"course_id": self.course.pk}

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "подписка удалена")
        self.assertFalse(Subscription.objects.filter(user=self.user, course=self.course).exists())
