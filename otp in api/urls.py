from django.urls import path
from .views_phone_login import SendOTPView, UserOTPLoginView

urlpatterns = [
    path('send/otp/', SendOTPView.as_view(), name='send_otp'),
    path('check/otp/', UserOTPLoginView.as_view(), name='check_otp'),
]