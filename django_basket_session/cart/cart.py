from decimal import Decimal
from shop.models import Products

CART_SESSION_ID = 'cart'                    #ایجاد یک سشن برای کارت
'''
cart
نشانه ای که ما به سشن ها اضافه میکنیم که از طریق آن سشن مربوط به کارت رو پیدا کنیم
(سشنهای مربوط به کارت خرید)به عبارت دیگر اسم سشنهای کربوطه رو کارت گذاشتیم
'''

class Cart:
    def __init__(self,request):
        self.session = request.session      #گرفتن  تمامی سشنهای وبسایت ما, مربوط به این کاربر در مرورگرش
        cart = self.session.get(CART_SESSION_ID)#گرفتن سشنی که مربوط به سبد خرید است
        if not cart:                        #اگر سشنی مربوط به کارت نبود
            cart = self.session[CART_SESSION_ID] = {}       # یک سشن مربوط به کارت با مقدار خالی بساز
        self.cart = cart                    #ذخیره کردن سشن کارتی و قرار دادن برای دسترسی بیشتر

    def __iter__(self):                     #برای بخش دیتیل کارت که بتونیم داخلش حلقه زده و محصولات رو نشون بدیم
        product_ids = self.cart.keys()      #گرفتن تمامی کلیدهای)(ایدی محصولات) موجود در سشن
        products = Products.objects.filter(id__in=product_ids)     #گرفتن تمامی محصولاتی که در سشن هستند
        cart = self.cart.copy()             #گرفتن کپی از کارت برای حفظ اطلاعات اصلی و انجام یکسری کارها بر روی آن
        for product in products:            #اضافه کردن فیلد پروداکت و قراردادن پروداکت درون آن برای همه محصولات سشن
            cart[str(product.id)]['product'] = product 

        for item in cart.values():          #محاسبه قیمت کل یک محصول باتوجه به مقدار و ذخیره آن در فیلد جدید توتال-پرایس
            item['total_price'] = Decimal(item['price']) * item['quantity']
            yield item
  
    def remove(self, product):              #حذف محصول از داخل کارت و سشن
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()
  
    def add(self, product, quantity):       # گرفتن محصول و ذخیره در سشن کارت کاربر
        product_id = str(product.id)        #ذخیره بصورت رشته چونکه در سشنها عدد خطا میده 
        if product_id not in self.cart:     #اگر محصول داخل کارت نبود
            self.cart[product_id] = {'quantity':0, 'price':str(product.price)} 
                                            #  نمونه محصول رو ذخیره کن با قیمت و تعداد درخواستی
        self.cart[product_id]['quantity'] += quantity    # اگر قبلا بود فقط مقادیرش رو اضافه کن
        self.save()                         # تغییرات رو ذخیره میکنیم

    def save(self):                         # در هربار تغییرات نیاز مند ذخیره میباشیم و این تابع ذخیره ساز است
        self.session.modified = True

    def get_total_price(self):              #جمع قیمت کل سفارش
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        del self.session[CART_SESSION_ID]
        self.save()









