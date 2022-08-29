from distutils.command.upload import upload
from django.db import models
from django.utils.text import slugify
from django.utils.crypto import get_random_string

# Create your models here.


class Tags(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class SeoIdModel(models.Model):
    seo_id = models.CharField(max_length=255, blank=True)
    seo_id_field = 'title'
    
    def get_seo_id(self):
        txt = ' '.join(getattr(self,self.seo_id_field).split()[:10])
        return slugify(txt,True)+'-'+get_random_string(length=8)

    def save(self,*args,**kwargs):
        if not self.seo_id:
            self.seo_id = self.get_seo_id()
        return super().save(*args,**kwargs)

    class Meta:
        abstract = True


class Post(SeoIdModel):
    tags = models.ManyToManyField(Tags)
    title = models.CharField(max_length=250)
    body = models.TextField()
    image = models.ImageField(upload_to = 'post/')
    is_active = models.BooleanField(default=False)
    is_remove = models.BooleanField(default=False)
    
    def __str__(self):
        return self.title
    
