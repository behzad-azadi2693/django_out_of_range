from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class MyUserManager(BaseUserManager):
    def create_user(self, username, password, phone_number, email):#method mudt have field necessery 
        if not email:#checking my fields
            raise ValueError('users must have Email')
        if not username:
            raise ValueError("user must have UserName")
        if not phone_number:
            raise ValueError("user must have Phone_Number")

        user = self.model(
                email=self.normalize_email(email),
                username=username,
                phone_number=phone_number
            )
        user.set_password(password)#hashing password for user
        user.save(using=self._db)#self._db is for get batabase active
        return user

    def create_superuser(self, username, password, phone_number, email):
        user = self.create_user(
                username=username,
                password=password,
                phone_number=phone_number,
                email=email
            )
        user.is_admin=True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150, unique=True)
    phone_number = models.CharField(max_length=11, unique=True)
    email = models.EmailField(max_length=150, blank=True, null=True)
    
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects=MyUserManager()#for use in self._db in manager

    USERNAME_FIELD = 'username' #this field must be unique=True
    REQUIRED_FIELDS = ['phone_number', 'email']

    def __str__(self):
        return f'{self.username}-{self.phone_number}'

    def has_perm(slef, perm, obj=None):#permisiions 
        return True

    def has_module_perms(self, app_label):#access to tables and data
        return True

    def is_staff(self):#access to panel admin
        return self.is_admin
