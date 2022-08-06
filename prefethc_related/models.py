from django.db import models

class A(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class B(models.Model):
    name = models.CharField(max_length=200)
    pulish = models.BooleanField(default=False)
    a_list = models.ForeignKey(A, on_delete=models.CASCADE, related_name='ball')

    def __str__(self):
        return f'{self.id}-{self.a_list.name}'
