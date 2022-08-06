from django.urls import path
from .views import add_user_order, basket, delete, order_payment, factor, verify ,send_request


app_name='eshop_orders'

urlpatterns = [
    path('user/', add_user_order, name='create'),      
    path('basket/buy/', basket , name='basket'),
    path('delete/<int:id>/', delete , name='delete'),
    #path('payment/', order_payment , name='send_request'),
    path('factor/', factor , name='factor'),
    path('request/<order_id>/', send_request, name='send_request'),
    path('verify/<order_id>/', verify , name='verify'),

]    