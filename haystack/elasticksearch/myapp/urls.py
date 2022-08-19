from django.urls import path
from .views import ElasticSearch1, ElasticSearch2

urlpatterns = [
    path('search1', ElasticSearch1.as_view()),
    path('search2', ElasticSearch2.as_view()),
]
