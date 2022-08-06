from django.contrib import admin

# Register your models here.
from .models import Order, OrderItem, Coupon


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_filter = ('active', 'valid_from', 'valid_to')
    list_display = ('active', 'valid_from', 'valid_to', 'discount', 'active')
    search_fields = ('code',)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ('product',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created', 'updated', 'paid')
    list_filter = ('paid',)
    inlines = (OrderItemInline, )