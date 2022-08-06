from pyexpat import model
import re
from django.contrib import admin
from .models import Photo
# Register your models here.
from django.template.loader import render_to_string
from django.utils.html import mark_safe

@admin.register(photo)
class PhotoAdmin(admin.ModelAdmin):
    def photo_show(self, obj):
        photo = render_to_string(
            "include/photo.html",
            {"photo":obj},
        )

        return mark_safe(photo)
    
    model = photo
    fields = ('id', 'photo_show', 'image')
    readonly_fields=('photo_show',)