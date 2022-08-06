from django.urls import path
from .views import index, detail


app_name = 'info'

urlpatterns = [
    path('', index, name='index'),
    path('<int:start>/<int:stop>/', test_host),
    path('information/parsing/pack/<int:pk>/', ParsingPackView, name='detail1'),
]
