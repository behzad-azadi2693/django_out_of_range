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

@login_required
def change_qty_pls(request):
    try:
        pk = request.GET.get('key_qty')
        obj = DataOne.objects.get(pk=pk)
        if request.user == obj.user:
            if obj.qty < obj.quantity:
                obj.qty += 1
                obj.save()
                obj_new = obj.qty
                return HttpResponse(obj_new)
            else:
                return JsonResponse({"error": "this quantity is not exists"}, status=400)
        else:
            return JsonResponse({"error": "this product is not in your order"}, status=400)
    except:
        return JsonResponse({"error": "this request is not safe"}, status=400)



def change_qty_mins(request):
    try:
        pk = request.GET.get('key_qty')
        obj = DataOne.objects.get(pk=pk)
        if request.user == obj.user:
            if obj.quantity > 0:
                obj.qty -= 1
                obj.save()
                obj_new = obj.qty
                return HttpResponse(obj_new)
            else:
                return JsonResponse({"error": "this quantity is nothing"}, status=400)
        else:
            return JsonResponse({"error": "this product is not in your order"}, status=400)
    except:
        return JsonResponse({"error": "this request is not safe"}, status=400)
