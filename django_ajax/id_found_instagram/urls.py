from django.urls import path
from .views import index, search_username,user_find

urlpatterns = [
    path('', index, name='index'),
    path('search/username/', search_username, name="search_username"),
    path('find/username/<str:name>/', user_find, name="user_find"),
]