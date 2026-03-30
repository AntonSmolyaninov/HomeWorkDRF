from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'users'

router = DefaultRouter()
router.register('payments', views.PaymentViewSet, basename='payment')
router.register('user-payments', views.UserPaymentViewSet, basename='user-payment')

urlpatterns = [
    path('', include(router.urls)),
]
