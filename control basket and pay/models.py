from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import Count, F, Value

class Product(models.Model):
    name = models.CharField(max_length=20)
    price = models.PositiveIntegerField()
    number = models.PositiveIntegerField()

    def __str__(self):
        return self.name

    @property
    def change_number(self):
        if self.number == 0:
            Order.objects.filter(product=self, status_pay='SE').delete()
        else:
            Order.objects.filter(product=self, number__gt=self.number, status_pay='SE').update(number=self.number )


class Basket(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    pay = models.BooleanField(default=False)
    go_to_pay = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.go_to_pay:
            Order.objects.filter(basket = self, status_pay = 'SE').update(status_pay = 'PA')

        if self.pay:
            Order.objects.filter(basket = self, status_pay = 'PA').update(status_pay = 'PU')

        super(Basket, self).save(*args, **kwargs)

    @property
    def cancle_pay(self):
        Order.objects.filter(basket = self, status_pay = 'PA').update(status_pay = 'SE')


class Order(models.Model):
    '''
        Will create a select box for this in the model form. Use can select from the
        options.The first element in each tuple is the actual value to be set on the model, 
        and the second element is the human-readable name. For example:
    '''
    STATUS_PAY = [
        (SE, 'SELECTED'),#انتخاب شده
        (PU, 'PURCHASED'),#خرید شده
        (PA, 'PAYING'),#در حال پرداخت
    ]

    basket = models.ForeignKey('Basket', on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING, null=True)
    number = models.PositiveIntegerField()
    status_pay = models.CharField(max_length=2, choices=STATUS_PAY, default='SE')

    def __str__(self):
        return f"{self.product.name}"
    
    def save(self, *args, **kwargs):
        htis = Order.objects.get(id = self.id)
        if this.status_pay == 'PA' and self.status_pay == 'SE':
            Product.objects.filter(id=self.product.id).update(number = F('number') + self.number)

        if self.status_pay == 'PA':
            product = Product.objects.get(id=self.product.id)
            product.number = F("product__number") - self.number
            product.save()
            product.change_number

        super(Order, self).save(*args, **kwargs)
