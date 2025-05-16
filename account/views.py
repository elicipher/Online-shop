from django.shortcuts import render , redirect
from django.views import View
from .forms import UserRegistrationForm , VerfyCodeForm
from django.contrib import messages
import random
from utils import send_otp_code
from .models import OtpCode , User
# Create your views here.

class UserRegisterView(View):
    form_class = UserRegistrationForm

    def get(self , request):
        form = self.form_class()
        return render(request , 'account/regiseter.html', {'form':form})

    def post(self , request):
        form = self.form_class(request.POST)
        if form.is_valid():
            print("information code :", form.cleaned_data)
            random_code = random.randint(1000 , 9999)
            send_otp_code(form.cleaned_data['phone_number'],random_code)
            print("RANDOM CODE", random_code)
            OtpCode.objects.create(phone_number =form.cleaned_data['phone_number'] , code =random_code)
            request.session['user_registration_info'] = {
                'phone_number': form.cleaned_data['phone_number'],
                'email': form.cleaned_data['email'],
                'full_name': form.cleaned_data['full_name'],
                'password': form.cleaned_data['password'],
            }

            messages.success(request , 'we send you a code','success')
            return redirect('account:verfy_code')
        else :
            messages.error(request , 'Registration failed.','danger')
            return redirect("home:home")
        
        
        
        

class VerfyCodeView(View):
    
    form_class = VerfyCodeForm
    def get(self , request):
        form = self.form_class()
        return render(request , 'account/verfy_code.html',{'form':form})

    def post(self , request):

        user_session = request.session['user_registration_info']
        code_instance = OtpCode.objects.get(phone_number = user_session['phone_number'])
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if cd['code'] == code_instance.code :
                User.objects.create_user(
                    user_session['phone_number'] , 
                    user_session['email'], 
                    user_session['full_name'],
                    user_session['password']
                                    )
                code_instance.delete()
                messages.success(request , 'you are registered' , 'success')
                return redirect("home:home")
            else :
                messages.error(request , 'this code is wrong' , 'danger')
                return redirect("account:verfy_code")
            
        return redirect("home:home") 
