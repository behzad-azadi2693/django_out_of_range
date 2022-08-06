from django.shortcuts import render
from django.contrib.auth import get_user_model
# Create your views here.
from .models import DataOne
from django.http import JsonResponse, HttpResponse
from django.core import serializers

def index(request):
    return render(request, 'index.html')



def check_username(request):
    username = request.GET.get('value')
    check = get_user_model().objects.filter(username=username).first()

    if check is not None:
        return JsonResponse({'check':'True'}, status=200)
    else:
        return JsonResponse({'check':'False'}, status=200)