from django.shortcuts import render
from .models import MyModel
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def index(request, pk):
    all_list = MyModel.objects.all()

    paginator = Paginator(all_list, 1)

    define = paginator.object_list.filter(pk=pk).first()
    id_list = list(paginator.object_list.values_list(flat=True))
    default_page = id_list.index(define.id) + 1
    
    page = request.GET.get('page', default_page)
    try:
        this_page = paginator.page(page)
    except PageNotAnInteger:
        this_page = paginator.page(1)
    except EmptyPage:
        this_page = paginator.page(paginator.num_pages)
     
    context = {
        'this_page':this_page,
    }

    if this_page.has_next():
        new = id_list[this_page.next_page_number() - 1]
        new_page = paginator.object_list.filter(pk=new).first()
        context['new_page'] = new_page

    if this_page.has_previous():
        old = id_list[this_page.previous_page_number() - 1]
        old_page = paginator.object_list.filter(pk = old).first()
        context['old_page'] = old_page
    
    return render(request, 'index.html', context)
