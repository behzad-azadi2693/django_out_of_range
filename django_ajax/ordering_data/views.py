from django.shortcuts import render

# Create your views here.
from .models import DataOne
from django.http import JsonResponse, HttpResponse
from django.core import serializers

def index(request):
    datas = DataOne.objects.all()
    context = {
        'datas':datas
    }
    return render(request, 'index.html', context)

def change(request):
    my_type = request.GET['keyname']

    if my_type == 'low':
        data = DataOne.objects.all().order_by('price')
    if my_type=='high':
        data = DataOne.objects.all().order_by('-price')
    else:
        pass

    data = serializers.serialize('json', data)

    #return HttpResponse(data, content_type="application/json")
    return JsonResponse({'datas': data}, status=200)
