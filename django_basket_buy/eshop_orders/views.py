from django.shortcuts import render, redirect
from .forms import UserNewOrderForm
# Create your views here.
from .models import Order, OrderDetail, OrderPayment
from eshop_product.models import Product
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import redirect
from zeep import Client


@login_required
def add_user_order(request):
    new_order_form = UserNewOrderForm(request.POST or None)

    if new_order_form.is_valid():
        product_id = new_order_form.cleaned_data.get('product_id')
        count = new_order_form.cleaned_data.get('count')

        product = Product.objects.get(id=product_id)

        order = Order.objects.filter(owner=request.user, is_paid=False).first()
        if order is None:
            order = Order.objects.create(owner=request.user)
        
        OrderDetail.objects.create(order=order, product = product, count = count)
        return redirect('eshop_orders:basket')
    return redirect('/')

@login_required
def basket(request):
    order = Order.objects.filter(owner=request.user, is_paid=False)

    context = {
        'orders':order,
    }

    return render(request, 'orders/basket.html', context)

@login_required
def factor(request):
    order = Order.objects.filter(owner=request.user, is_paid=True)

    context = {
        'orders':order,
    }

    return render(request, 'orders/factor.html', context)

#for test payment
@login_required
def order_payment(request):
    order = Order.objects.filter(owner=request.user, is_paid=False).first()
    if order:
        orders_details = OrderDetail.objects.filter(order=order)

        for order_detial in orders_details:
            order_pyment =  OrderPayment.objects.create(
                order=order,
                product=order_detial.product,
                price=order_detial.product.price,
                count=order_detial.count
            )

        order.is_paid = True
        order.payment_date = datetime.now()
        order.save()
        orders_details.delete()
        return redirect('eshop_orders:factor')
    return redirect('eshop_orders:basket')

@login_required
def delete(request, id):
    order = Order.objects.get(id=id)

    if order.owner == request.user and order.is_paid == False:
        order.delete()
        return redirect('eshop_orders:basket')
    return redirect('eshop_orders:basket')



MERCHANT = 'XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX'
client = Client('https://www.zarinpal.com/pg/services/WebGate/wsdl')
amount = None  # Toman / Required
description = "درگاه پرداخت فروشگاه ما"  # Required
#email = 'email@example.com'  # Optional
#mobile = '09123456789'  # Optional
CallbackURL = 'http://localhost:8000/verify' # Important: need to edit for realy server.

def send_request(request, *args, **kwargs):
    order_id = kwargs.get('order_id')
    if order_id is not None:
        order = Order.objects.filter(owner=request.user, is_paid=False).first()
        if order is not None:
            amount = order.total_price()
    
    result = client.service.PaymentRequest(MERCHANT, amount, description, request.user.email, request.user.mobile, f'{CallbackURL}/{order.id}')
    if result.Status == 100:
        return redirect('https://www.zarinpal.com/pg/StartPay/' + str(result.Authority))
    else:
        return HttpResponse('Error code: ' + str(result.Status))


def verify(request, *args, **kwargs):
    order_id = kwargs.get('order_id ')
    if request.GET.get('Status') == 'OK':
        result = client.service.PaymentVerification(MERCHANT, request.GET['Authority'], amount)
        if result.Status == 100:
            order = Order.objects.get_queryset().get(id=order_id)
            if order:
                orders_details = OrderDetail.objects.filter(order=order)

                for order_detial in orders_details:
                    order_pyment =  OrderPayment.objects.create(
                        order=order,
                        product=order_detial.product,
                        price=order_detial.product.price,
                        count=order_detial.count
                    )

                order.is_paid = True
                order.payment_code = result.RefID
                order.payment_date = datetime.now()
                order.save()
                orders_details.delete()
            return HttpResponse('Transaction success.\nRefID: ')
        elif result.Status == 101:
            return HttpResponse('Transaction submitted : ')
        else:
            return HttpResponse('Transaction failed.\nStatus: ')
    else:
        return HttpResponse('Transaction failed or canceled by user')