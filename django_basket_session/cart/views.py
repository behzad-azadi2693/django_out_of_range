from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from .cart import Cart
from shop.models import Products
from .forms import CartAddForm
from django.views.decorators.http import require_POST



def detail(request): #نمایش جزییات سبد خرید کاربر
    cart = Cart(request)
    # مقذار سلف.سشن رو , که حاوی سشن کاربر بخش های مربوط به کارت خرید رو به ما برمیگردونه
    context = {
        'cart':cart,
    }


    return render(request, 'cart/detail.html', {'cart':cart})


@require_POST
def cart_add(request, product_id): 
    # اضافه کردن یک محصول به سبد خرید(این ویو وظیفه ارسال اطلاعات به فایل کارت برای ذخیره در سشن)
    cart = Cart(request)
    prd = get_object_or_404(Products, pk=product_id)
    form = CartAddForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=prd, quantity=cd['quantity'])
    return redirect('cart:detail')


def cart_remove(request, product_id):
    #در این ویو اقدام به حذف یک محصول از داخل کارت رو انجام میدیم
    cart = Cart(request)
    product = get_object_or_404(Products, id=product_id)
    cart.remove(product)
    return redirect('cart:detail')