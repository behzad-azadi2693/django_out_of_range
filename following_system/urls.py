from django.urls import path
from .views import follow, unfollow
app_name='account'

urlpatterns = [
    path('follow/', follow, name='follow'),
    path('unfollow/', unfollow , name='unfollow'),
]