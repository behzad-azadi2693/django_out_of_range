from django.urls import path
from . import views

app_name = 'orders'


urlpatterns = [
    path('create/', views.order_create, name='create'),
    path('order_detail/', views.order_detai, name='order-detail'),
    path('order_paid/', views.order_paid, name='paid'),
    path('order_delete/<int:id>/', views.order_delete, name='delete'),
    #path('payment/<int;order_id>/<price>/', ....),
    #path('verify/', ....),
    path('apply/<int:order_id>/', views.coupon, name='coupon'),
]