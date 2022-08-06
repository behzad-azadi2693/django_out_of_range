from django import forms



class CartAddForm(forms.Form): 
    # برای ارسال تعداد(مقادیر) خرید یک محصول به درون سبد این فرم درون اپ مربوط به نمایش محصول قرار میگیرد
    quantity = forms.IntegerField(
        min_value=1, 
        max_value=9, 
    )
