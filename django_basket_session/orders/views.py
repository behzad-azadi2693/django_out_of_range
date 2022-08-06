from django.shortcuts import render, get_object_or_404, redirect, get_list_or_404

# Create your views here.
from django.contrib.auth.decorators import login_required
from .models import Order, OrderItem, Coupon
from cart.cart import Cart
from .forms import CouponForm
from django.utils import timezone
from django.views.decorators.http import require_POST



@login_required
def order_create(request):
    cart=Cart(request)
    if cart.get_total_price() != 0:
        order = Order.objects.create(user=request.user)
        for item in cart:
            OrderItem.objects.create(order=order, product=item['product'], price=item['price'], quantity=item['quantity'])
        cart.clear()
        return redirect('orders:order-detail')
    return redirect('shop:index')



@login_required
def order_delete(request, id):
    order = get_object_or_404(Order, id=id)

    if order.user == request.user and order.paid == False:
        order.delete()
        return redirect('orders:order-detail')
    return redirect('orders:order-detail')


@login_required
def order_detai(request):
    orders = Order.objects.filter(user = request.user, paid=False)

    context = {
        'orders':orders,
        'form':CouponForm
    }
    return render(request, 'orders/orders_detail.html', context)


@login_required
def order_paid(request):
    orders = Order.objects.filter(user = request.user, paid=True)

    context = {
        'orders':orders,
    }
    return render(request, 'orders/orders_paid.html', context)

@require_POST
def coupon(request, order_id):
    now = timezone.now()
    form = CouponForm(request.POST)
    if form.is_valid():
        code = form.cleaned_data['code']
        try:
            coupon = Coupon.objects.get(code__iexact=code, valid_from__lte=now, valid_to__gte=now, active=True)

        except Coupon.DoesNotExist:
            messages.error(request, 'this coupon not exsits', 'danger')
            return redirect('orders:detail')
        order = Order.objects.get(id=order_id)
        order.discount = coupon.discount
        order.save()
    return redirect('orders:detail')