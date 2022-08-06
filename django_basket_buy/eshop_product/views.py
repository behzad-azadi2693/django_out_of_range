from django.shortcuts import render, get_object_or_404
from eshop_orders.forms import UserNewOrderForm
# Create your views here.
from .models import Product


def index(request):
    product = Product.objects.all()

    context = {
        'products':product,
    }

    return render(request, 'shop/index.html', context)


def detail(request, slug):
    product = get_object_or_404(Product, slug=slug)

    context = {
        'prd':product,
        'form':UserNewOrderForm(initial={'product_id':product.id})
    }

    return render(request, 'shop/detail.html', context)