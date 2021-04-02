from django.models import models
from django.contrib.auth.models import User

class Relation(models.Model):
    from_user = models.ForiegnKey(User, on_delete=models.CASCAD)
    to_user = models.ForiegnKey(User, on_delete = models.CASCAD)
