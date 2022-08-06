from django.urls import path
from . import views


app_name='eshop_product'

urlpatterns = [
    path('', views.index, name='index'),
    path('detail/<slug>/', views.detail , name='detail'),
]