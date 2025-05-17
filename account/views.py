from django.shortcuts import render , redirect
from django.views import View
from .forms import UserRegistrationForm , VerfyCodeForm
from django.contrib import messages
import random
from utils import send_otp_code
from .models import OtpCode , User
from datetime import timedelta, datetime, timezone 
# Create your views here.

class UserRegisterView(View):
    form_class = UserRegistrationForm
    template_name = 'account/regiseter.html'
    def get(self , request):
        user_data = request.session.get('user_registration_info')
        form = self.form_class(initial=user_data) if user_data else self.form_class()
        # if user_data:
        #     form = self.form_class(initial=user_data)
        # else:
        #     form = self.form_class()

        return render(request , self.template_name, {'form':form})
    
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
            return render(request , self.template_name, {'form':form})
        
        
        
        

class VerfyCodeView(View):
    
    form_class = VerfyCodeForm
    def get(self , request):
        form = self.form_class()
        return render(request , 'account/verfy_code.html',{'form':form})
    
    def post(self , request):
        
        user_session = request.session['user_registration_info']
        try:
            code_instance = OtpCode.objects.get(phone_number=user_session['phone_number'])
        except OtpCode.DoesNotExist:
            messages.error(request , 'No code found. Try again.' , 'danger')
            return redirect("account:user_register")
        
        form = self.form_class(request.POST)

        if code_instance.is_expired():
            code_instance.delete()
            messages.error(request , 'The code has expired. Try again.' , 'danger')
            return redirect("account:user_register")
        
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
