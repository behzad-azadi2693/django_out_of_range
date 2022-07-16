from django.db import models

# Create your models here.


class FileUser(models.Model):
    name = models.CharField(max_length=200)
    my_file = models.FileField(upload_to='file/')
