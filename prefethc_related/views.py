from django.shortcuts import render
from .models import A, B
from django.db import connection, reset_queries
from django.db.models import Prefetch, Subquery



def debugger(func):
    def wrapper(*args, **kwargs):
        reset_queries()
        start_time = time.time()
        value = func(*args, **kwargs)
        end_time = time.time()
        queries = len(connection.queries)
        print(f"------------------connection number: {queries}----time: {start_time-end_time}")
        return value
    return wrapper


def index(request):
    a_s = A.objects.prefetch_related(Prefetch('ball', queryset=B.objects.filter(pulish=True))).all()
    
    return render(request, 'index.html', {'as':a_s})
