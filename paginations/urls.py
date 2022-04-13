from django.urls import path
from.views import index

urlpatterns = [
    path('<int:pk>/', index, name='index'),
]
