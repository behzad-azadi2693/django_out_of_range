from django.shortcuts import render
from zipfile import ZipFile
from rarfile import RarFile
import os

# Create your views here.
from .models import FileUser

def index(request):
    all = FileUser.objects.all()
    return render(request, 'index.html', context={'all':all})



def detail(request, pk):
    obj = FileUser.objects.get(id=pk)
    fileName, fileExtension = os.path.splitext(obj.my_file.name)

    if fileExtension == '.rar':
        with RarFile(obj.my_file, 'r') as rarObj:
            listOffile = rarObj.infolist()
            all = [(element.filename,element.file_size) for element in listOffile]
    
    if fileExtension == '.zip':
        with ZipFile(obj.my_file, 'r') as zipObj:
            listOffile = zipObj.infolist()
            all = [(element.filename,element.file_size) for element in listOffile]
    

    return render(request, 'detail.html', context={'obj': obj, 'all':all})
