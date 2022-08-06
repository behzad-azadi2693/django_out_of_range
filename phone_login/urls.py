from django.urls import path
from .views import phone_login, verify


app_name='accounts'

urpatterns = [
    path('phone_login/', phone_login, name='phone_login'),
    path('verify/', verify , name='verify'),
]