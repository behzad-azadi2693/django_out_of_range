import ast
from datetime import datetime, timedelta
from urllib import parse

time = datetime.now() + timedelta(hours=4)

def get_list_key_cart(request, key):
    if request.COOKIES.get('item_cart'):
        get_item_cart_in_cookie = request.COOKIES['item_cart']
        
        str_convert_to_list = list(get_item_cart_in_cookie.split(';'))
        key_list = []
        if key == 'quantity':
            for obj in str_convert_to_list:
                index_convert_to_dict = ast.literal_eval(obj)
                key_list.append(int(index_convert_to_dict[key])
        else:
            for obj in str_convert_to_list:
                index_convert_to_dict = ast.literal_eval(obj)
                key_list.append(str(index_convert_to_dict[key]))
        
        return key_list


def len_item_in_cart(request):
    if request.COOKIES.get('item_cart'):
        list_item = get_list_key_cart(request, "item")
        return len(list_item)

    return 0

def check_item_in_cart(request, item):
    if str(item) in get_list_key_cart(request, "item"):
        return True

    else:
        return False
                                
def check_obj_in_cart(request, key_str):
    items = get_list_key_cart(request, "item")
    sizes = get_list_key_cart(request, "size")
    colors = get_list_key_cart(request, "color")
    key_list = []
    for index in len(items):
        key = f'{items[index]}-{sizes[index]}-{colors[index]}'
        key_list.append(key)
                                
    if str(key_str) in key_list:
        return True
    else:
        return False
                                
def add_to_cart(request, response, item, quantity=1, size=None, color=None):
    if request.COOKIES.get('item_cart') is not None:
        key_str = f'{item}-{size}-{color}'
        if not check_obj_in_cart(request, key_str):
            item_in_cookie = request.COOKIES['item_cart']
            new_item = {"item":item,"quantity":quantity, "size":size, "color":color}
            data = item_in_cookie+f';{new_item}'
            response.set_cookie('item_cart', data, expires=time)
            
            number = request.COOKIES['item_count']
            number = int(number)+1
            response.set_cookie('item_count', number, expires=time)

    else:
        new_item = {"item":item,"quantity":quantity, "size":size, "color":color}
        data = f'{new_item}'
        response.set_cookie('item_cart', data, expires=time)
        response.set_cookie('item_count', 1, expires=time)

def create_sequence_str(request, items, quantities, sizes, colors):
    str_ = "first"
    for index in range(len_item_in_cart(request)):
        if index < 1:
            new_item = {"item":keys[index],"quantity":quantities[index], "size":sizes[index], "color":colors[index]}
            if index < 1:
                str_ = f'{new_item}'
            else:    
                str_ = str_+f';{new_item}'
        
    return str_

def delete_item_in_cart(request, response, item):
    if request.COOKIES.get('item_cart'):
        if check_item_in_cart(request, item):
            if len_item_in_cart(request) > 1:
                items = get_list_key_cart(request,"item")
                quantities = get_list_key_cart(request, "quantity")
                sizes = get_list_key_cart(request, "size")
                colors = get_list_key_cart(request, "color")

                index = keys.index(item)
                del items[index] 
                del quantities[index]
                del sizes[index]
                del colors[index]
                data = create_sequence_str(request, items, quantities, sizes, colors)
                response.set_cookie('item_cart', data, expires=time)

                number = request.COOKIES['item_count']
                number = int(number)-1
                response.set_cookie('item_count', number, expires=time)

            else:
                response.delete_cookie('item_cart')
                response.delete_cookie('item_count')

def delete_cart(request, response):
    if request.COOKIES.get('item_cart'):
        response.delete_cookie('item_cart')
        response.delete_cookie('item_count')

def update_quantity_item_cart(request, response, item, quantity):
    if request.COOKIES.get('item_cart') is not None:
        if check_item_in_cart(request, key_str):
            items = get_list_key_cart(request, "item")
            quantities = get_list_key_cart(request, "quantity")
            sizes = get_list_key_cart(request, "size")
            colors = get_list_key_cart(request, "color")

            index = keys.index(item)    
            quantities[index] = quantity
                             
            data = create_sequence_str(request, items, quantities, sizes, colors)
            response.set_cookie('item_cart', data, expires=time)

def incr_one_to_quantity(request, response, item):
    if request.COOKIES.get('item_cart') is not None:
        if check_item_in_cart(request, item):
            items = get_list_key_cart(request, "item")
            quantities = get_list_key_cart(request, "quantity")
            sizes = get_list_key_cart(request, "size")
            colors = get_list_key_cart(request, "color")
            
            index = keys.index(item)
            quantities[index] = quantities[index] + 1

            data = create_sequence_str(request, items, quantities, sizes, colors)
            response.set_cookie('item_cart', data, expires=time)

def dicr_one_to_quantity(request, response, item):
    if request.COOKIES.get('item_cart') is not None:
        if check_item_in_cart(request, item):
            items = get_list_item_cart(request)
            quantities = get_list_quantities_cart(request)
            sizes = get_list_key_cart(request, "size")
            colors = get_list_key_cart(request, "color")
                                
            index = keys.index(item)
            quantities[index] = quantities[index] - 1

            data = create_sequence_str(request, items, quantities, sizes, colors)
            response.set_cookie('item_cart', data, expires=time)

def get_information_user_encode(request, response, address, phone):
    if request.COOKIES.get('item_cart') is not None:
        informatino = {'آدرس':address,'تلفن':phone}
        data = parse.quote(f'{informatino}')
        response.set_cookie('item_address', data, expires=time)

def get_information_user_decode(request):
    if request.COOKIES.get('item_address') is not None:
        information = request.COOKIES['item_address']
        return parse.unquote(information)
      
      
'''
def my_function(request):
    .
    .
    .
    context = {
        ....
    }
    response = render(request, template, context)

    cart_cookie.every_function(*args, **kwargs)

    return response
'''
#github = https://github.com/joeliberal/django_out_of_range/blob/master/cart_cookies.py
