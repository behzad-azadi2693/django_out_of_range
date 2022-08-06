from django import forms
from .models import User
from django.contrib.auth.forms import ReadOnlyPasswordHashField

#this for adminn.py
class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='confirm password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'username', 'phone_number')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] and cd['password2'] and cd['password1'] != cd['password2']:
            raise forms.ValidationError('passworsd must match')
        return cd['password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()
    class Meta:
        model = User
        fields = ('email', 'password', 'username', 'phone_number')

    def clean_password(self):
        return self.initial['password']





#this for template and views
messages = {
    'required': 'این فیلد الزامیست',
    'invalid': 'صحیحی نمیباشد ',
    'max_length' : 'اندازه مجاز نیست',
    'min_length' : 'اندازه کم است'
}


class UserLoginForm(forms.Form):
    username = forms.CharField(
            label= 'نام کاربری',
            error_messages=messages, 
            max_length=150,
            min_length= 10,
            widget=forms.TextInput(attrs={'class':'form-control'})
        )
    password = forms.CharField(
            label= 'پسورد',
            error_messages=messages, 
            widget=forms.PasswordInput(attrs={'class':'form-control'})
        )



class UserRegisterForm(forms.Form):
    username = forms.CharField(
            label= 'نام کاربری',
            error_messages=messages, 
            max_length=150,
            widget=forms.TextInput(attrs={'class':'form-control'})
        )
    password = forms.CharField(
            label= 'پسورد',
            error_messages=messages, 
            widget=forms.PasswordInput(attrs={'class':'form-control'})
        )
    phone_number = forms.CharField(
            label= 'تلفن',
            max_length=11,
            error_messages=messages, 
            widget=forms.TextInput(attrs={'class':'form-control'})
        )
    email = forms.EmailField(
            label='ایمیل',
            error_messages=messages,
            max_length=150,
            widget=forms.EmailInput(attrs={'class':'form-control'})
        )

    def clean_username(self):
        username = self.cleaned_data['username']
        user = User.objects.filter(username=username)
        if user.exists():
            raise forms.ValidationError('نام کاربری تکراری است')
        return username

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        user = User.objects.filter(phone_number=phone_number)
        if user:
            raise forms.ValidationError('شماره تلفن تکراری است')
        return phone_number



class UserUpdateForm(forms.ModelForm):
    class Meta:    
        model = User
        fields= ['username', 'email', 'phone_number', 'password']
        widgets = {
            'phone_number':forms.TextInput(attrs={'class':'form-control'}),
            'username':forms.TextInput(attrs={'class':'form-control'}),
            'email':forms.EmailInput(attrs={'class':'form-control'}),
            'password':forms.PasswordInput(attrs={'class':'form-control'}),
        }
        help_texts = {
                'password':'بسیار امن انتخاب کنید*' ,
                'email' : 'معتبر باشد*',
                'username': 'تکراری نباشد*',        
            }
        error_messages = {
                'phone_number':{ 
                    'required': 'فیلد تلفن الزامیست',
                    'max_length' : 'شماره تلفن یازده رقم باید باشد',
                    'min_length' : 'شماره تلفن نباید کمتر از ۱۱ رقم باشد',
            },
            'usernmae':{ 
                    'required': 'فیلد تلفن الزامیست',
                    'max_length' : 'نام کاربر زیاد است',
                    'min_length' : 'نام کاربر کوتاه است',
            },
            'email':{ 
                    'required': 'فیلد تلفن الزامیست',
                    'invalid' : 'صحیح نیست',
                    'max_length' : 'ایمیل طولانی است',
                    'min_length' : 'ایمیل کوتاه است',
            },
            'password':{ 
                    'required': 'فیلد  الزامیست',
            },
        }
        labels = {
            'phone_number': 'شماره تلفن' ,
            'password' : 'پسورد' ,
            'email' : 'ایمیل' ,
            'username' : 'نام کاربری' ,
        }


    def clean_username(self):
        username = self.cleaned_data['username']
        user = User.objects.filter(username=username)
        if user.exists():
            raise forms.ValidationError('نام کاربری تکراری است')
        return username

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        user = User.objects.filter(phone_number=phone_number)
        if user:
            raise forms.ValidationError('شماره تلفن تکراری است')
        return phone_number