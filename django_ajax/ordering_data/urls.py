from django.urls import path
from .views import index,change,change_qty

urlpatterns = [
    path('', index, name='index'),
    path('ajax/change/', change, name='change'),
]