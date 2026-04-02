from django.urls import include, path
from rest_framework.permissions import AllowAny
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from users.apps import UsersConfig
from users.views import UserCreateAPIView

from . import views

app_name = "users"

router = DefaultRouter()
router.register("payments", views.PaymentViewSet, basename="payment")
router.register("user-payments", views.UserPaymentViewSet, basename="user-payment")

urlpatterns = [
    path("", include(router.urls)),
    path("register/", UserCreateAPIView.as_view(), name="register"),
    path(
        "login/",
        TokenObtainPairView.as_view(permission_classes=(AllowAny,)),
        name="Login",
    ),
    path(
        "token/refresh/",
        TokenRefreshView.as_view(permission_classes=(AllowAny,)),
        name="token_refresh",
    ),
    path("list/", views.UserListAPIView.as_view(), name="list"),
    path("<int:pk>/", views.UserRetrieveUpdateDestroyAPIView.as_view(), name="detail"),
]
