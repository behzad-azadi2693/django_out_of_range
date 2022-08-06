from django.db import models

# Create your models here.


class a(models.Model):
    title = models.CharField(max_length=100)

class b(models.Model):
    title = models.CharField(max_length=100)