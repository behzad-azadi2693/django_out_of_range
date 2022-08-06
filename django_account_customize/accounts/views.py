from django.shortcuts import render, redirect

# Create your views here.
from .forms import UserLoginForm, UserRegisterForm, UserUpdateForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .models import User


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            cd = form.changed_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None:
                login(request, user)
                messages.success(request , 'uo loging', 'success')
                return redirect('shop:home')
            else:
                messages.error(request, 'password or username denaid', 'danger')
    else:
        form = UserLoginForm()
    return render(request, 'accounts/login.html', {'form':form})



def user_register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = User.objects.create_user(cd['username'],cd['password'],cd['phone_number'],cd['email'])
            user.save()
            messages.success(request, 'you are register', 'success')
            user_inc = authenticate(request, username=cd['username'], password=cd['password'])
            login(request, user_inc)
            return redirect('shop:home')
    else:
        form = UserRegisterForm()
    return render(request, 'accounts/register.html', {'form':form})


def user_logout(request):
    logout(request)
    messages.success(request, 'you are logout', 'success')
    return redirect('shop:home')

def user_update(request):
    user = User.objects.get(pk=request.user.pk)
    password_old= user.password

    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            cd = form.cleaned_data        
            user.username = cd['username']
            user.email = cd['email']
            if cd['password'] is not None:
                user.set_password(cd['password'])
            else:
                user.password = password_old
            user.phone_number = cd['phone_number']
            user.save()
    else:
        form = UserUpdateForm(instance=user)
    return render(request, 'accounts/update.html', {'form':form})