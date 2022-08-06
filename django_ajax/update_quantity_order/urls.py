from django.urls import path
from .view import index, change_qty_pls


urlpatterns = [
    path('', index, name="index"),
    path('change/quantity/plus/', change_qty_pls, name="change_qty_pls"),
]