from django.db import models

# Create your models here.


class Tags(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Post(models.Model):
    tag = models.ManyToManyField(Tags)
    title = models.CharField(max_length=250)
    body = models.TextField()
    technical_tips = models.TextField()

    def __str__(self):
        return self.title
