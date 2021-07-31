from .forms import PhoneLoginForm, VerifyForm
from random import randint
from .models import Profile
from django.contrib.auth.models import User
from kevenegar import KavenegarAPI

def phone_login(request):

    if request.method == 'POST':
        form = PhoneLoginForm(request.POST)
        if form.is_valid():
            global phone, rand_num 
            phone = f'0{form.cleaned_data['number']}'
            rand_num = randint(1000, 9999)
            api = KavenegarAPI('Your APIKey', timeout=20)
            params = {'sender':'numer_get_of_kavenegar', 'receptor':phone, 'message':rand_num}
            api.sms_send(params)
            return redirect('accounts:verify')
    else:
        form = PhoneLoginForm()
    return render(request, 'number.html', {'form':form})


def verify(request):
    if request.method == 'POST':
        form = VerifyForm(request.POST)
        if form.is_valid():
            if rand_num == form.cleaned_data['code']:
                user = get_object_or_404(User, profile__phone=phone)
                login(request, user)
                return redirect('posts':'list')
            else:
                message.error(request, 'you code wrong', 'warning')
    else:
        form = VerifyForm()
    return render(request, 'verify.html', {'form':form})
