from django.db import models
from uuid import uuid4
# Create your models here.


class Products(models.Model):
    price = models.IntegerField()
    image = models.ImageField(upload_to='media/')
    title = models.CharField(max_length=200)
    slug = models.SlugField(default=uuid4, unique=True, editable=False) 
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.title