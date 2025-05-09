from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from .managers import UserManager
# Create your models here.
class User(AbstractBaseUser):
    email = models.EmailField(max_length=255 , unique=True)
    phone_number = models.CharField(max_length=11 , unique=True)
    full_name = models.CharField(max_length=150)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'phone_number' #Login with number
    REQUIRED_FIELDS = ['email','full_name'] #just for createsuperuser

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
    
#Otpcode : one time code for login
class OtpCode(models.Model):
    phone_number = models.CharField(max_length=11)
    code = models.PositiveSmallIntegerField()
    created = models.DateField(auto_now=True)

    def __str__(self):
        return f'{self.phone_number} - {self.code}'


