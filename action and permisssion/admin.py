from django.contrib import admin
from .models import Post
from django.http import HttpResponse
from django.core import serializers


def export_as_json(modeladmin, request, queryset):
    response = HttpResponse(content_type = 'application/json')
    serializers.serialize('json', queryset, stream=response)
    return response
export_as_json.short_description = 'Export to json'


def make_publish(modeladmin, request, queryset):
    result=queryset.update(status='published')
    if result == 1:
        message_bit = '1 post changed'
    else:
        message_bit = f'{result} posts changed'
    modeladmin.message_user(request, f'{message_bit} successfully change to publish')
make_publish.short_description = 'change object status to publish'from django.contrib import admin


class mymodelAdmin(admin.ModelAdmin):    
    list_display = ('display_gener', 'display_gener1')

    def display_gener1(self, obj):
        return ', '.join([gener.name for gener in obj.gener.all()[:3]])
    display_gener1.short_description = 'Gener1'

