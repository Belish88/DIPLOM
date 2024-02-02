from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from django.urls import path

from app_users.apps import AppUsersConfig
from app_users.views import RegisterUserAPIView, phone, code, ProfileAPIView

app_name = AppUsersConfig.name

urlpatterns = [
    path('register/', RegisterUserAPIView.as_view(), name="register"),
    path('phone/', phone, name="phone"),
    path('code/', code, name="code"),
    path('token/', TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path('token/refresh/', TokenRefreshView.as_view(), name="token_refresh"),
    path('profile/<int:pk>/', ProfileAPIView.as_view(), name='profile'),

]
