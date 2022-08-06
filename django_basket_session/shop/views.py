from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.views.generic import ListView
from .models import Products
from cart.forms import CartAddForm


def index(request):
    pro = Products.objects.all()
    context = {
        'products':pro,
    }

    return render(request, 'shop/index.html', context)



def detail(request, slug):
    product = get_object_or_404(Products, slug=slug)

    context = {
        'prd':product,
        'form':CartAddForm
    }

    return render(request, 'shop/detail.html', context)