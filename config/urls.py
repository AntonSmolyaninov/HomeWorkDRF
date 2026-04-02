from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import include, path


def redirect_to_courses(request):
    """Перенаправление на список курсов"""
    return redirect("/materials/courses/")


urlpatterns = [
    # Админка
    path("admin/", admin.site.urls),
    # Корневой URL - перенаправление на курсы
    path("", redirect_to_courses, name="home"),
    # API для материалов (курсы и уроки)
    path("materials/", include("materials.urls", namespace="materials")),
    # API для пользователей и платежей
    path("users/", include("users.urls", namespace="users")),
]

# Добавляем поддержку медиафайлов в режиме разработки
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
