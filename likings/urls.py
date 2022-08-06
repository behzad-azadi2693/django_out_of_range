from django.url import path
from .views import post_like, detail
app_name='post'

urlpatterns = [
    path('detail/<int:pk>/', detail , name='detail'),
    path('like/<int:post_id>/', post_like, name='vote'),
]