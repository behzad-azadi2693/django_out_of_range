from .models imort Home
from .choice import price, type


def search(request):
    query = Home.objects.all()order_by('-time')

    if 'country' in request.GET:
        country = request.GET['contry']
        query = query.filter(country__iexact=country)

    if 'city' in request.GET:
        city = request.GET['city']
        query = query.filter(city__icontains=city)

    if 'price' in request.GET:
        price = request.GET['price']
        query = query.filter(price__lte=price)

    if 'type' in request.GET:
        type = request.GET['type']
        query = query.filter(type__exact=type)

    context = {
        'price':price,
        'type':type,
        'query':query,
        'old_value':request.GET
    }

    return render(request, 'search.html', context)