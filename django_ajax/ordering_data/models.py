from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.

class DataOne(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    family = models.CharField(max_length=100)
    price = models.IntegerField()

    def __str__(self):
        return self.name
