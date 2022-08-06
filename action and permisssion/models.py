from django.db import models
from django.db.models.base import Model

class my_models(models.Model):
    .
    gener = models.ManyToManyField(.....)
    status = models.CharField(.....)


    def display_gener(self): #for admin pannel
        return ', '.join([gener.name for gener in self.gener.all()[:3]])
    display_gener.short_description = 'Gener'

    class Meta:
        permissions = (
            ("can_show_views","CSV"),
            ("can_read_this","CRT",),
        )