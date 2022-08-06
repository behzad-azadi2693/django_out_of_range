from django.urls import path
from .views import index, check_username

urlpatterns = [
    path('', index, name='index'),
    path('check/username/', check_username, name="check_username"),
]