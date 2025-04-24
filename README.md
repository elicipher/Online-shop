# 👤 Custom User Model with UserManager in Django

این پروژه از یک مدل کاربر سفارشی همراه با `UserManager` استفاده می‌کند تا ثبت‌نام کاربران بر اساس شماره تلفن انجام شود.

## 📁 ساختار فایل‌ها
project/ │ ├── accounts/ │ ├── models.py │ ├── managers.py │ └── ... ├── manage.py └── README.md 


---

## ❓ چرا از مدل کاربر سفارشی استفاده کردیم؟

در پروژه‌هایی که ثبت‌نام و ورود کاربران باید با فیلدی به‌جز نام کاربری یا ایمیل انجام شود (مثلاً شماره تلفن)، مدل پیش‌فرض Django مناسب نیست.  
برای همین از یک **مدل کاربر کاستوم‌شده** استفاده کردیم که:
- ورود کاربران با شماره تلفن انجام شود (`USERNAME_FIELD = 'phone_number'`)
- فیلدهایی مثل `full_name` و `email` هم به‌صورت اجباری باشند
- امکان توسعه و شخصی‌سازی‌های بیشتر در آینده را فراهم کند (مثل اضافه‌کردن نقش‌ها، پروفایل پیشرفته و ...)

---

## ⚙️ UserManager چیست؟

`UserManager` یک کلاس مدیریت کاربران است که برای تعریف متدهای سفارشی مثل `create_user` و `create_superuser` استفاده می‌شود.

💡 **نکته مهم:**  
از آنجایی که مدل کاربر را خودمان نوشته‌ایم (`CustomUser`) و آن را از `AbstractBaseUser` به ارث برده‌ایم، منیجر پیش‌فرض متدهای `create_user` و `create_superuser` را ندارد. بنابراین باید خودمان این متدها را در کلاس `UserManager` پیاده‌سازی کنیم.

---

### 🧱 کد مربوطه:

```python
# managers.py

from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):
    #We can create custom methods.

    def create_user(self , phone_number , email ,full_name, password ):
        if not phone_number:
            raise ValueError("User must be have phone number")
        if not email :
            raise ValueError("User must be have email")
        if not full_name:
            raise ValueError("User must be full name")
        
        #Django validates the password.

        #creates a new user object form the model class connected to the manager. 
        user = self.model(phone_number = phone_number, email = self.normalize_email(email) ,full_name = full_name ) 
        user.set_password(password)
        user.save(using = self._db)#save the user in the database
        return user
    
    def create_superuser(self , phone_number , email , full_name , password):

        user = self.create_user(phone_number ,email , full_name , password)
        user.is_admin = True
        user.save(using = self._db)
        return user

```

## 🛠️ اتصال منیجر به مدل
در فایل models.py، کلاس کاربر باید به این صورت از منیجر استفاده کند:
```python

#modes.py
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
```


