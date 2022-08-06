from django.shortcuts import render
from .models import a,b
from django.http import JsonResponse, HttpResponse
# Create your views here.
def index(request):
    return render(request, 'index.html')

def search(request,cat):
    name = request.GET.get('text')
    print(name)
    return render(request, 'index.html')

def ajax_search(request):
    word = request.GET.get('word')
    A = a.objects.filter(title__icontains=word)
    B = b.objects.filter(title__icontains = word)

    if A and B:
        datas = ['a','b']
        return JsonResponse({'datas':datas}, status=200)
    elif A:
        datas = ['a',]
        return JsonResponse({'datas':datas}, status=200)

    elif B:
        datas = ['b',]
        return JsonResponse({'datas':datas}, status=200)
    else:
        return JsonResponse(status=400)