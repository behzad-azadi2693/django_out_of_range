from django.shortcuts import render
from django.contrib.auth import get_user_model
# Create your views here.
from .models import DataOne
from django.http import JsonResponse, HttpResponse
from django.core import serializers

def index(request):
    return render(request, 'index.html')



def search_username(request):
    username = request.GET.get('value')
    users = get_user_model().objects.filter(username__contains=username)
    if users:
        datas = serializers.serialize('json', users)
        return JsonResponse({'datas':datas}, status=200)
    else:
        return Http404()

def user_find(request, name):
    pass