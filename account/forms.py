from django import forms
from .models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField

class UserCreationForm(forms.ModelForm):#we will use in admin panel
    password1 = forms.CharField(label='Password' , widget=forms.PasswordInput) 
    password2 = forms.CharField(label='Confrim password' , widget=forms.PasswordInput) 
    class Meta:
        model = User
        fields = ['email','phone_number','full_name']

    def clean_password2(self): #we use password2 because it errors if the password1 in not exists
        cd = self.cleaned_data
        if cd['password1'] and cd['password2'] and cd ['password1'] != cd['password2']:
            raise ValidationError('passowrds must be match')
        return cd['password2']
    
    def save(self , commit = True):
       user = super().save(commit = False)
       user.set_password(self.cleaned_data['password1'])
       if commit :
           user.save()
        
       return user

class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(help_text = "you can change password using <a href = \"../password/\" > this form</a>.")
    
    class Meta:
        model = User
        fields = ['email','phone_number','full_name' , 'password','last_login']

class UserRegitrationForm(forms.Form):
    email = forms.EmailField(max_length=255)
    phone_number = forms.CharField(max_length=11)
    full_name = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

