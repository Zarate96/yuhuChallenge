from django.urls import path
from .views import UserRegistrationView

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path("user/login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("user/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path('user/register/', UserRegistrationView.as_view(), name='user-register'),
]
