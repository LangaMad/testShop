from django.urls import path
from .views import UserRegistration, UserLogin

urlpatterns = [
    path('api/register/', UserRegistration.as_view(), name='user-registration'),
    path('api/login/', UserLogin.as_view(), name='user-login'),
]
