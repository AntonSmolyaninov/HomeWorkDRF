from django.urls import path
from rest_framework.routers import SimpleRouter

from materials.apps import MaterialsConfig
from materials.views import (CourseViewSet, LessonCreateAPIView,
                             LessonDestroyAPIView, LessonListAPIView,
                             LessonRetrieveAPIView, LessonUpdateAPIView,
                             SubscriptionAPIView, UserSubscriptionsView)

app_name = MaterialsConfig.name

# Роутер для курсов (ViewSet)
router = SimpleRouter()
router.register("courses", CourseViewSet)  # Курсы доступны по /courses/

urlpatterns = [
    # Маршруты для уроков (Generic)
    path("lessons/", LessonListAPIView.as_view(), name="lesson-list"),
    path("lessons/<int:pk>/", LessonRetrieveAPIView.as_view(), name="lesson-detail"),
    path("lessons/create/", LessonCreateAPIView.as_view(), name="lesson-create"),
    path(
        "lessons/update/<int:pk>/", LessonUpdateAPIView.as_view(), name="lesson-update"
    ),
    path(
        "lessons/delete/<int:pk>/", LessonDestroyAPIView.as_view(), name="lesson-delete"
    ),
    path("subscribe/", SubscriptionAPIView.as_view(), name="subscription"),
    path("my-subscriptions/", UserSubscriptionsView.as_view(), name="my-subscriptions"),
]

urlpatterns += router.urls
