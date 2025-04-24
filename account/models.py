from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from .managers import UserManager
# Create your models here.
class User(AbstractBaseUser):
    email = models.EmailField(max_length=255 , unique=True)
    phone_number = models.CharField(max_length=11 , unique=True)
    full_name = models.CharField()
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = ['phone_number'] #Login with number
    REQUIRED_FIELDS = ['email'] #just for createsuperuser

    objects = UserManager() #Using our manager or customized 

    def __str__(self):
        return self.email
    
    def has_perm(self , perm , obj = None):
        return True
    
    def has_module_perms(self,app_label):
        return True
    
    @property#وقتی یه متد رو با @property علامت می‌زنی، می‌تونی اون متد رو مثل یه ویژگی (attribute) صدا بزنی، نه مثل یه تابع.
    def is_staff(self):
        return self.is_admin