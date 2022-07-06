#refrences
#https://django.cowhite.com/blog/mastering-search-in-django-postgres/
#https://www.netlandish.com/blog/2020/06/22/full-text-search-django-postgresql/



from django.shortcuts import render
from .models import Book


#==================================SearchSimple=============================

def simple_search(request):
    book = Book.objects.filter(name__containse = 'name')

    return render(request, template_name, {'books':books})



#=============================FullTextSearchSimple==========================

from django.db.models import Q

def simple_full_text_serchh(request):
    '''
    (1)این ساده ترین روش برای جستجوی یک عبارت واحد در برابر یک ستون واحد در پایگاه داده است
    (2)برای جستجوی یک عبارت واحد در برابر چند ستون از چند فیلتر
    (3)یا عبارت کیو استفاده میکنیم
    *** اما برای جستجوی یک عبارت واحد در برابر چند ستون بهتر است که از سرچ وکتور استفاده کنیم ***
    '''

    #1
    books = Book.objects.filter(name__search = 'name')

    #2
    books = Book.objects.filter(name__search='name', author__name__search='name')
    books = Book.objects.filter(name__search='name1').filter(author__name__search='name2')

    #3
    books = Book.objects.filter(Q(name__search='name') | Q(author__name__search='name'))
    books = Book.objects.filter(Q(name__search='name1') & Q(author__name__search='name2'))

    return render(request, template_name, {'books':books})



#=============================SearchVectore=================================

from django.contrib.postgres.search import SearchVector

def search_vector(request):
    '''
    برای پرس و جو در برابر چندین ستون
    آرگومان های سرچ وکتور می توانند هر عبارت یا نام یک فیلد باشند
    (1)چندین آرگومان با استفاده از یک فاصله به یکدیگر متصل می شوند تا سند جستجو شامل همه آنها باشد
    (2)اشیاء سرچ وکتور را می توان با هم ترکیب کرد و به شما امکان استفاده مجدد از آنها را می دهد
    '''

    #1
    books = Book.objects.annotate(
            search = SearchVector('title', 'author__name'),
        ).filter(search='name')

    #2
    books = Book.objects.annotate(
            search = SearchVector('title') + SearchVector('author__name'),
        ).filter(search='name')

    return render(request, template_name, {'books':books})



#=============================SearchQueiesy=================================

from django.contrib.postgres.search import SearchQuery, SearchVector

def search_vectore_with_query(request):
    '''
    سرچ کوری عبارات را به یک شی پرس و جوی جستجو ترجمه می کند که پایگاه داده با بردار جستجو مقایسه می کند
    مزیت استفاده از سرچ کوری این است که به‌طور پیش‌فرض تمام کلمات ارائه‌شده قبل از جستجوی عبارت‌های منطبق،
    (1)از طریق یک الگوریتم پایه ارسال می‌شوند.بنابراین یک نتیجه جستجوی بسیار مرتبط برای استفاده از آن کلمه ارائه می شود.
    (2)یکی دیگر از مزایای استفاده از سرچ کوری این است که می‌توانیم به راحتی با استفاده از اند و اور و نات ترکیب منطقی کنیم .
    '''

    #1
    books = Book.objects.annotate(
            search=SearchVector('title') + SearchVector('author__name'),
        ).filter(search = SearchQuery('name'))

    #2
    books = Book.objects.annotate(
            search=SearchVector('title') + SearchVector('author__name'),
        ).filter(search = SearchQuery('name1') & SearchQuery('name2'))   

    return render(request, template_name, {'books':books})


    ***
    search_type متد سرچ کوری پارامتری میگیرد بنام 
    در چهار نوع زیر دسته بندی میشند
    
    بصمورت پیش فرض بر روی این نوع قرار دارد و رشته قابل سرچ را بصورت عبارات جداگانه در نظر میگیرد plain
    این نوع تمامی رشته رو یک عبارت واحد در نظر گرفته و سرچ میکند phrase
    این نوع به شما اجازه میدهد که جستجویی با عملگرها داشته باشید raw
    این نوع دقیقا مشابه موتورهای جستجو وب عمل میکند که از ورژن ۱۱ پستگرس به بعد اضافه شده است wbsearch
    ***
    
    #plain
    SearchQuery('firstname lastname') >> 'firstname','lastname' دو بخش جداگانه
    
    #phrase
    SearchQuery('firstname lastname' ,search_type='phrase') >> 'firstname lastname' یک عبارت کامل
    
    #raw
    SearchQuery("'this' & ('name1' | 'name2')" ,search_type='raw') >> 'this name1' or 'tihs name2'
    
    #websearch
    SearchQuery("'this' ('name1' or 'name2')" ,search_type='websearch') >> جستجو مانند موتورهای جستوی وب
    
    
    
#=====================================SearchRank=======================================

from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector


def search_rank(request):
    '''
    سرچ رانک نتایج را بر اساس ارتباط آن با عبارت(های) جستجوی ارائه شده توسط کاربر مرتب می کند.
    پستگرس یک تابع رتبه بندی را ارائه می دهد که تعداد دفعات ظاهر شدن عبارات پرس و جو در سند،
    (1)نزدیکی عبارات در سند به یکدیگر و اهمیت بخشی از سند در محل وقوع آنها را در نظر می گیرد. رتبه با تطابق بهتر بالاتر است.
    هر فیلد ممکن است ارتباط یکسانی در یک پرس و جو نداشته باشد، بنابراین می توانید وزن بردارهای مختلف را قبل از ترکیب آنها تنظیم کنید.
    ما می‌توانیم 4 سطح وزن را به هر سرچ وکتور [ای، بی، سی، یا دی] اختصاص دهیم که 'ای' دارای بیشترین وزن است، طبق قرارداد
    در سرچ رانک می‌توانیم وزن‌های واقعی را برای هر یک از حروف ذکر شده در بالا با ارسال مقدار وزن‌های آرگومان به عنوان لیستی از 4 عدد شناور تعیین کنیم.
    (2)وزن های پیش فرض (اگر آرگومان وزن ها را در سرچ رانک پاس نکنید) این حروف هستند
    D->0.1، C->0.2، B->0.4، A->1.0
    '''

    #1
    vector = SearchVector('title', 'descriptions')
    query = SearchQuery('name')

    books = Book.objects.annotate(
            rank=SearchRank(vector, query)
        ).order_by('-rank')


    #2
    vector = SearchVector('title', weight='A') + SearchVector('author__name', weight='B')
    query = SearchQuery('name')

    books = Book.objects.annotate(
            rank=SearchRank(vector, query)
        ).filter(rank__gte=0.3).order_by('-rank')
    
    return render(request, template_name, {'books':books})




#=====================================SearchVectorField=======================================
'''
برای استفاده از هر یک از عملکردهای بالا، نیازی به تغییر پایگاه داده خاصی نیست.
اما از آنجایی که جستجوی متن کامل فرآیندی پرمصرف و سنگین است،
ممکن است هنگام جستجوی بیش از چند صد رکورد با مشکل مواجه شود.
واقعیتی که باید به آن توجه داشت این است که پایگاه داده ها در واقع برای جستجوی متن کامل طراحی نشده اند.
برای کاهش این مشکل تا حدی می توانید فهرست هایی برای جستجوی متن کامل ایجاد کنید که در مستندات پستگرس مستند شده است.
روش دیگری که حتی بهتر کار می کند اضافه کردن سرچ وکتورفیلد به مدل شما است.
برای مثال، همانطور که در مستندات پستگرس توضیح داده شده است، باید آن را با تریگرها پر کنید.
سپس می توانید فیلد را جویا شوید که گویی یک سرچ رانک مشروح شده است:
'''

#model.py
from django.db import models
from django.contrib.postgres.search import SearchVector, SearchVectorField      
from django.contrib.postgres.indexes import GinIndex

class Book(models.Model):
    title = models.CharField(max_length=200)
    search_field = SearchVectorField(null=True)

    class Meta:
        indexes = [
            GinIndex(fields=["search_field"])]
        
#tasks.py in task celery     
Book.objects.update(search_field=SearchVector('title'))
دقت کنید که تبدیل یک رشته به یک مقدار سرچ وکتور کار زمانی بری هست 
لذا با استفاده از سیگنال و سلری آن را در بکند انجام دهید

#views.py in view search
Book.objects.filter(search_field='name')


#=====================================TrigramSimilarity=======================================

from django.contrib.postgres.search import TrigramSimilarity, TrigramDistance

def trigram_similarity_search(request):
    '''
    تعداد تریگرام ها یا سه نویسه متوالی را که بین عبارت(های) جستجو و متن مورد نظر به اشتراک گذاشته شده اند مقایسه می کند.
    pg_trgm اطمینان حاصل کنید از نصب بودن اکستنشن مورد نیاز در پستگرس
    TrigramSimilarity , TrigramDistance در اینجا دو تابع مکمل وجود دارد که عبارتند از 
    هر دو اساساً اطلاعات یکسانی را ارائه می دهند، 
    اما یکی مقدار شباهت و دومی مقدار تفاوت را برمی گرداند.
    '''
    
    test = 'sentence'
    
    # Similarity
    books = Book.objects.annotate(
            similarity=TrigramSimilarity('title', test),
        ).filter(similarity__gt=0.3).order_by('-similarity')

    # Distance
    books = Book.objects.annotate(
            distance=TrigramDistance('title', test),
        ).filter(distance__lte=0.3).order_by('distance')

    return render(request, template_name, {'books':books})
