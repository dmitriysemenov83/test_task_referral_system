from django.urls import path

from users.apps import UsersConfig
from users.views import PhoneNumberAuthAPIView, VerifyCodeAPIView, UserProfileAPIView

app_name = UsersConfig.name

urlpatterns = [
    path('auth/phone/', PhoneNumberAuthAPIView.as_view(), name='phone_auth'),
    path('auth/verify/', VerifyCodeAPIView.as_view(), name='verify_code'),
    path('profile/', UserProfileAPIView.as_view(), name='user_profile'),
]