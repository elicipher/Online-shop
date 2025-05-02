from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserChangeForm , UserCreationForm
from .models import User , OtpCode
from django.contrib.auth.models import Group
# Register your models here.

class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    form_add = UserCreationForm #the second form

    list_display = ('full_name','phone_number','is_admin')
    list_filter = ('is_admin',)
    #fieldsets is used to define the layout of the admin form
    fieldsets = (
        ('Main',{'fields':('email','phone_number','full_name','password')}),
        ('Permissions',{'fields':('is_active','is_admin','last_login')})
    )#for UserChangeForm

    add_fieldsets = (
        (None ,{'fields':('phone_number' , 'email' , 'full_name' , 'password1', 'password2')}),
    )#for UserCreationForm

    search_fields = ('email','full_name')
    ordering = ('full_name' , 'last_login')
    filter_horizontal = ()

#un-register django admin group 
admin.site.unregister(Group)
#register UserAdmin
admin.site.register(User, UserAdmin)

@admin.register(OtpCode)
class OtpCodeAdmin(admin.ModelAdmin):
    list_display = ('phone_number','code','created')

