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



#----------------------------------------python
import os
from zipfile import ZipFile
from rarfile import RarFile
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import BasePermission
import subprocess
import json

class ParsingPackPermision(BasePermission):
    def has_permission(self, request, view):
        if request.GET.get('path', None) is None:
            return False
        return True


      
      
class ParsingPackView(APIView):
    permission_classes = [ParsingPackPermision]

    def get(self, request, *args, **kwargs):
        file_path = request.GET['path']
        fileName, fileExtension = os.path.splitext(file_path.split('/')[-1])

        if fileExtension == '.rar' and os.path.isfile(file_path):
            try:
                all = {}

                with RarFile(str(file_path), 'r') as rarObj:
                    listOffile = rarObj.infolist()

                    for element in listOffile:
                        try:
                            all[element.filename.split('/')[-1]] = element.file_size
                        except:
                            pass

                all = dict(sorted(all.items(),key=lambda item:item[1], reverse=True))

                return Response(all, status=200)
            except:
                return Response({'msg':'There was a problem parsing the package'}, status=400)

        if fileExtension == '.zip' and os.path.isfile(file_path):
            try:
                all = {}

                with ZipFile(str(file_path), 'r') as zipObj:
                    listOffile = zipObj.infolist()

                    for element in listOffile:
                        try:
                            all[element.filename.split('/')[-1]] = element.file_size
                            
                        except:
                            pass


                all = dict(sorted(all.items(),key=lambda item:item[1], reverse=True))

                return Response(all, status=200)
            except:
                return Response({'msg':'There was a problem parsing the package'}, status=400)
        
        if fileExtension == '.7z' and os.path.isfile(file_path):
            try:
                all_name = list(subprocess.check_output("py7zr l {path_file} | sed '1,3d' | cut -d '/' -f 2 |\
                    grep -v '-' | grep -v '^ ' |  tr ' ', '_' | tr '\n', ','".format(
                    path_file=str(file_path)),shell=True).decode('utf8').split(','))

                all_size = list(subprocess.check_output("py7zr l {path_file} | sed '1,3d' | awk '{code};' |\
                    grep -v '-'".format(path_file=str(file_path), code="{print $4}"),shell=True).decode('utf8').split('\n'))


                all = {}
                for name,size in zip(all_name, all_size):
                    try:
                        all[str(name.replace('_', ' '))] = int(int(size))
                    except:
                        pass


                all = dict(sorted(all.items(),key=lambda item:item[1], reverse=True))

                return Response(all, status=200)
            
            except:
                return Response({'msg':'There was a problem parsing the package'}, status=400)


        else:
            return Response({'msg':'package do not support'}, status=400)
        
  
#----------------------------------------new------------------------------
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
from zipfile import ZipFile
from rarfile import RarFile
from .models import Post
import subprocess
import requests
import json
import os


def parsing_pack(file_path, fileExtension):
    
    if fileExtension == '.rar':
        try:
            all = {}
            with RarFile(file_path, 'r') as rarObj:
                listOffile = rarObj.infolist()
                for element in listOffile:
                    try:
                        all[element.filename.split('/')[-1]] = element.file_size
                    except:
                        pass
            all = dict(sorted(all.items(),key=lambda item:item[1], reverse=True))
            return all
        except:
            return False

    if fileExtension == '.zip':
        try:
            all = {}
            with ZipFile(str(file_path), 'r') as zipObj:
                listOffile = zipObj.infolist()
                for element in listOffile:
                    try:
                        all[element.filename.split('/')[-1]] = element.file_size
                    except:
                        pass
            all = dict(sorted(all.items(),key=lambda item:item[1], reverse=True))
            return all
        except:
            return False
        
    if fileExtension == '.7z' and os.path.isfile(file_path):
        try:
            all_name = list(subprocess.check_output("py7zr l {path_file} | sed '1,3d' | cut -d '/' -f 2 |\
                grep -v '-' | grep -v '^ ' |  tr ' ', '_' | tr '\n', ','".format(
                path_file=str(file_path)),shell=True).decode('utf8').split(','))
            all_size = list(subprocess.check_output("py7zr l {path_file} | sed '1,3d' | awk '{code};' |\
                grep -v '-'".format(path_file=str(file_path), code="{print $4}"),shell=True).decode('utf8').split('\n'))
            all = {}
            for name,size in zip(all_name, all_size):
                try:
                    all[str(name.replace('_', ' '))] = int(int(size))
                except:
                    pass
            all = dict(sorted(all.items(),key=lambda item:item[1], reverse=True))
            return all
        except:
            return False


      
def ParsingPackView(request, pk):
    obj = get_object_or_404(Post, id=pk)
    exists_path = 'gallery/parsing_data/'+f'{obj.id}.json'
    if not os.path.isfile(exists_path):
        file_path = obj.public_pack.path
        fileName,fileExtension  = os.path.splitext(file_path.split('/')[-1])
        if os.path.isfile(file_path) and fileExtension in ['.rar', '.zip', '.7z']:
            dictionary_data = parsing_pack(str(file_path), fileExtension)
            if dictionary_data is not False:
                try:
                    with open(exists_path,"x") as f:
                         pass
                    with open(exists_path, "w") as parsing_write:
                        json.dump(dictionary_data, parsing_write)
                    return JsonResponse(dictionary_data, status=200)
                except:
                    return JsonResponse({'msg':'create file json or writing file json with error'}, status=400)
            else:
                return JsonResponse({'msg':'data parsing not working'}, status=400)
        else:   
            return JsonResponse({'msg':'path pack not in server or pack not in rar,zip,7z'}, status=400)
    else:
        try:
            with open(exists_path, "r") as pkl_handle:
                dictionary_data = json.load(pkl_handle)
            return JsonResponse(dictionary_data, status=200)
        except:
            return JsonResponse({'msg':'reading file information with error'}, status=400)


def test_host(request, start, stop):
    range_id = [i for i in range(start, stop+1, 1)]
    all_post = Post.objects.filter(id__in = range_id).order_by('id')
    information_of_query = {}

    for post in all_post:
        exists_path = 'gallery/parsing_data/'+f'{post.id}.json'

        if not os.path.isfile(exists_path):
            public_path = post.public_pack.path

            if os.path.isfile(public_path):
                information_of_query[str(post.id)] = 'package is into server'
                requests.get(f'https://boomilia.com/gallery/information/parsing/pack/{post.id}/')

            else:
                try:
                    file_path = post.url
                    fileName, fileExtension = os.path.splitext(file_path.split('/')[-1])
                    page = requests.get(file_path)

                    save_pack = f'gallery/parsing_data/this_file{fileExtension}'

                    with open(save_pack, 'wb') as file:
                        file.write(page.content)

                    dictionary_data = parsing_pack(str(save_pack), fileExtension)

                    with open(exists_path,"x") as f:
                         pass
                    with open(exists_path, "w") as parsing_write:
                        json.dump(dictionary_data, parsing_write)

                    information_of_query[str(post.id)] = 'package is into host arvancloud'
                    os.remove(save_pack)
                    
                except:
                    information_of_query[str(post.id)] = 'warning for this package'
        else:
            information_of_query[str(post.id)] = 'package befor parsing data'

    return JsonResponse(information_of_query, status=200)

            
    
    
    
#------------------------------python/linux

from genericpath import isfile
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Post
import subprocess
import json
import os


def parsing_pack(file_path, fileExtension):
    
    if fileExtension == '.rar':
        try:
            all = {}

            all_name = list(
                subprocess.check_output("unrar t {path_file} | sed '1,7d' | sed '$d' | cut -d' ' -f 6- |\
            tr 'OK' ' ' | rev | sed  -e 's/^[ \t]*//' | cut -d '/' -f -1 | rev | awk '{code};' |tr '\n' ','".format(
                path_file=str(file_path), code="{print $1}"),shell=True).decode('utf8').split(',')
            )

            all_size = list(
                subprocess.check_output("unrar l {path_file} | sed '1,8d' | sed '$d' |\
                sed '$d' | sed '$d' | awk '{code};'".format(
                path_file=str(file_path), code="{print $2}"),shell=True).decode('utf8').split('\n')
            )

            for name,size in zip(all_name, all_size):
                try:
                    all[str(name)] = int(int(size))
                except:
                    pass

            drcending_sort= dict(sorted(all.items(),key=lambda item:item[1], reverse=True))
            remove_value_zero = {x:y for x,y in drcending_sort.items() if y!=0}

            return remove_value_zero
        
        except:
            return False
    
    elif fileExtension == '.zip':
        try:
            all = {}

            all_name = list(
                subprocess.check_output("zip -sf {path_file} | sed '1d' | sed '$d' |\
                sed -e 's/^[ \t]*//' | tr ' ' '_' | tr '\n' ','".format(
                path_file=str(file_path)),shell=True).decode('utf8').split(',')
            )
            
            all_size = list(
                subprocess.check_output("unzip -l {path_file} | sed '1,3d' |  sed '$d' |\
                awk '{code};' | grep -v '-'".format(
                path_file=str(file_path), code="{print $1}"),shell=True).decode('utf8').split('\n')
            )

            for name,size in zip(all_name, all_size):
                try:
                    all[str(name.split('/')[-1])] = int(int(size))
                except:
                    pass

            drcending_sort= dict(sorted(all.items(),key=lambda item:item[1], reverse=True))
            remove_value_zero = {x:y for x,y in drcending_sort.items() if y!=0}

            return remove_value_zero
        
        except:
            return False
        
    elif fileExtension == '.7z':
        try:
            all = {}

            all_name = list(
                subprocess.check_output("py7zr l {path_file} | sed '1,3d' | cut -d '/' -f 2 |\
                grep -v '-' | grep -v '^ ' |  tr ' ', '_' | tr '\n', ','".format(
                path_file=str(file_path)),shell=True).decode('utf8').split(',')
            )

            all_size = list(
                subprocess.check_output("py7zr l {path_file} | sed '1,3d' | awk '{code};' |\
                grep -v '-'".format(
                path_file=str(file_path), code="{print $4}"),shell=True).decode('utf8').split('\n')
            )

            for name,size in zip(all_name, all_size):
                try:
                    all[str(name.replace('_', ' '))] = int(int(size))
                except:
                    pass

            drcending_sort= dict(sorted(all.items(),key=lambda item:item[1], reverse=True))
            remove_value_zero = {x:y for x,y in drcending_sort.items() if y!=0}

            return remove_value_zero

        except:
            return False

    else:
        return False
      

def parsing_pack_view(request, pk):
    obj = get_object_or_404(Post, id=pk)
    local_path = 'gallery/parsing_data/'+f'{obj.id}.json'
    file_path = obj.public_pack.path
    fileName,fileExtension  = os.path.splitext(file_path.split('/')[-1])

    if fileExtension not in ['.rar', '.zip', '.7z']:
        return JsonResponse({'msg':'format file not supported'}, status=400)

    if os.path.isfile(local_path):
        try:
            with open(local_path, "r") as pkl_handle:
                dictionary_data = json.load(pkl_handle)
                
            return JsonResponse(dictionary_data, status=200)

        except:
            return JsonResponse({'msg':'reading file information with error'}, status=400)

    if os.path.isfile(file_path):
        dictionary_data = parsing_pack(str(file_path), fileExtension)

        if dictionary_data is not False:
            try:
                with open(local_path,"x") as f:
                     pass

                with open(local_path, "w") as parsing_write:
                    json.dump(dictionary_data, parsing_write)

                return JsonResponse(dictionary_data, status=200)

            except:
                return JsonResponse(dictionary_data, status=200)

        else:
            return JsonResponse({'msg':'parsing data with error'}, status=400)

    else: 
        host_path = '/mnt/ftp/home3/' + file_path.split('/')[-1]
        dictionary_data = parsing_pack(str(host_path), fileExtension)

        if dictionary_data is not False:
            try:
                with open(local_path,"x") as f:
                     pass

                with open(local_path, "w") as parsing_write:
                    json.dump(dictionary_data, parsing_write)

                return JsonResponse(dictionary_data, status=200)

            except:
                return JsonResponse(dictionary_data, status=200)

        else:
            return JsonResponse({'msg':'parsing data with error or hosting error'}, status=400)
    

