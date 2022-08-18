from pyexpat import model
from statistics import mode
from django.db import models

# Create your models here.
class Customer(models.Model):
    title = models.CharField(max_length=200)
    descriptions = models.TextField()
 
    def __str__(self) -> str:
        return self.title
 