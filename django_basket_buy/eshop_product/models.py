from django.db import models
from uuid import uuid4
# Create your models here.

class Product(models.Model):
    image = models.ImageField(upload_to='media')
    name = models.CharField(max_length=100)
    slug = models.SlugField(default=uuid4 , unique=True)
    price = models.IntegerField()
    title = models.CharField(max_length=250)
    

    def __str__(self):
        return self.name 