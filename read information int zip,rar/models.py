from django.db import models

# Create your models here.
class Post(models.Model):
    name = models.CharField(max_length=200)
    public_pack = models.FileField(upload_to='file/')
    url = models.URLField(null=True)


    class Meta:
        ordering = ('-name',)
