from django.contrib import admin

# Register your models here.
from .models import Order, OrderDetail, OrderPayment

admin.site.register(OrderPayment)

class OrderDetailInline(admin.TabularInline):
    model = OrderDetail


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderDetailInline,]
    list_display = ['owner', 'payment_date', 'is_paid']
    list_filter = ['owner', 'is_paid']