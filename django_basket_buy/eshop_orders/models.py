from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from eshop_product.models import Product


class Order(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    is_paid = models.BooleanField(default=False)
    payment_date = models.DateTimeField(null=True, blank=True)
    total_payment = models.IntegerField(null=True, blank=True)
    payment_code = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return f'{self.owner.username}'

    def total_price(self):
        amount = 0
        for detail in self.relord.all():
            amount += detail.product.price * detail.count
        return amount

    def total_price_payment(self):
        amount = 0
        for detail in self.relpay.all():
            amount += detail.price * detail.count
        return amount
        
class OrderDetail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='relord')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    count = models.IntegerField()

    def price(self):
        return self.product.price 

    def total_price(self):
        return self.count * self.product.price


    def __str__(self):
        return f'{self.order}'


class OrderPayment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='relpay')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.IntegerField()
    count = models.IntegerField()

    def total_price(self):
        return self.price * self.count


    def __str__(self):
        return f'{self.order}'