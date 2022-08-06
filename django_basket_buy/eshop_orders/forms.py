from django import forms

class UserNewOrderForm(forms.Form):
    product_id = forms.IntegerField(widget=forms.HiddenInput)
    count = forms.IntegerField(min_value=1, widget=forms.NumberInput(attrs={'class':'form-control w-25 '}), initial=1)