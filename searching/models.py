

class Home(models.Model):
    image = models.ImageField()
    country = models.CharField(max_length=100)
    city = models.CharField(max_length='100')
    price = models.IntegerField()
    number = models.IntegerFields()
    time = models.DateTime(auto_now_add=True)