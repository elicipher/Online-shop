from django.shortcuts import render , redirect
from django.views import View
from .forms import UserRegitrationForm
from django.contrib import messages
import random
from utils import send_otp_code
from .models import OtpCode
# Create your views here.

class UserRegisterView(View):
    form_class = UserRegitrationForm

    def get(self , request):
        form = self.form_class()
        return render(request , 'account/regiseter.html', {'form':form})

    def post(self , request):
        form = self.form_class(request.POST)
        if form.is_valid():

            random_code = random.randint(1000 , 9999)
            send_otp_code(self.cleaned_data['phone_number'],random_code)
            OtpCode.objects.create(phone_number =self.cleaned_data['phone_number'] , code =random_code)
            request.session['user_registration_info'] = {

            'phone_number': self.cleaned_data['phone_number'],
            'email': self.cleaned_data['email'],
            'full_name': self.cleaned_data['full_name'],
            'password': self.cleaned_data['password'],
            }

            messages.success(request , 'we send you a code','success')
            return redirect('account:verfy_code')
        return redirect("home:home")

class VerfyCodeRegistrationView(View):
    def get():
        pass

    def post():
        pass
