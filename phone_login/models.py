from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneFiled(User, on_delete=models.CASCAD)
    phone = models.IntegerField(max_lentgh=11)