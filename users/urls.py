from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from users.apps import UsersConfig
from users.views import PaymentListAPIView, UserViewSet

app_name = UsersConfig.name

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users')

urlpatterns = [
                  path('login/', TokenObtainPairView.as_view(), name='login'),
                  path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
                  path('payments/', PaymentListAPIView.as_view(), name='payment_list'),
              ] + router.urls
