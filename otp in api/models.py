from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.
class User(AbstractUser):
    sms_verification_token = models.CharField(max_length=15,unique=True,blank=True,default=None,null=True)

    phone = PhoneNumberField('phone number' ,unique = True,null = True,default = None,blank = True ,
                error_messages={'unique': "A user with that phone already exists.",} 
            )

    username = models.CharField('username',max_length=150,unique=True,
            help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.',
            validators=[AbstractUser.username_validator],
            error_messages={'unique': "A user with that username already exists.",},
        )