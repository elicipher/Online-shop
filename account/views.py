from django.shortcuts import render , redirect
from django.views import View
from .forms import UserRegistrationForm , VerfyCodeForm , LoginForm
from django.contrib import messages
import random
from .tasks import send_otp_code_task
from .models import OtpCode , User
from django.contrib.auth import login ,authenticate , logout
from django.contrib.auth.mixins import LoginRequiredMixin


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
            random_code = random.randint(1000 , 9999)
            print("otp code ",random_code)
            send_otp_code_task.delay("عضویت",form.cleaned_data['phone_number'],random_code)
            OtpCode.objects.filter(phone_number = form.cleaned_data['phone_number']).delete()
            OtpCode.objects.create(phone_number =form.cleaned_data['phone_number'] , code =random_code)
            request.session['user_registration_info'] = {
                'phone_number': form.cleaned_data['phone_number'],
                'email': form.cleaned_data['email'],
                'full_name': form.cleaned_data['full_name'],
                'password': form.cleaned_data['password'],
            }
            request.session['purpose'] = 'register'

            messages.success(request , 'we send you a code','success')
            return redirect('account:verify_code')
        else :
            return render(request , self.template_name, {'form':form})
        

class LoginView(View):
    def setup(self, request, *args, **kwargs):
        self.next = request.GET.get('next')
        return super().setup(request, *args, **kwargs)
    
    def dispatch(self, request, *args, **kwargs):
        if  request.user.is_authenticated :
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)
    
    form_class = LoginForm
    template_name = 'account/login_page.html'

    def get(self , request):
        form = self.form_class()
        return render(request , self.template_name , {'form': form})

    def post(self , request):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = authenticate(request , phone_number = form.cleaned_data["phone_number"] , password = form.cleaned_data["password"])
            if user :
                request.session['user_registration_info']={
                    'phone_number': form.cleaned_data['phone_number'],
                    'password':form.cleaned_data['password']
                }
                request.session['purpose'] = 'login'
                random_code = random.randint(1000 , 9999)
                send_otp_code_task.delay("ورود",form.cleaned_data['phone_number'],random_code)
                OtpCode.objects.filter(phone_number = form.cleaned_data['phone_number']).delete()
                OtpCode.objects.create(phone_number = form.cleaned_data['phone_number'] ,code = random_code)
                messages.success(request , 'we send you a code','success')
                return redirect('account:verify_code')
            else :
                messages.error(request , "Password or number phone is wrong" , 'danger')
                return render(request , self.template_name , {'form': form})
        
        return render(request , self.template_name , {'form': form})

class LogoutView(LoginRequiredMixin, View):
       
       def get(self,request):
        logout(request)
        messages.success(request , "You logout successfuly " , "success")
        return redirect('home:home')


class VerfyCodeView(View):
    form_class = VerfyCodeForm

    def get(self, request):
        form = self.form_class()
        return render(request, 'account/verify_code.html', {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        user_session = request.session.get('user_registration_info')
        purpose = request.session.get('purpose')  # 'register' یا 'login'

    
        phone_number = user_session.get('phone_number')
    
        try:
            code_instance = OtpCode.objects.get(phone_number=phone_number)
        except OtpCode.DoesNotExist:
            messages.error(request, 'No code found. Try again.', 'danger')
            return redirect("account:verify_code")

       

        if code_instance.check_and_delete_if_expired():
            code_instance.delete()
            messages.error(request, 'The code has expired. Try again.', 'danger')
 
            if purpose == 'register':
                return redirect("account:user_register")
            else :
                return redirect("account:user_login")

        if form.is_valid():
            cd = form.cleaned_data
            if cd['code'] == code_instance.code:
                if purpose == 'register':
                    registered_user = User.objects.create_user(
                        phone_number=user_session['phone_number'],
                        email=user_session['email'],
                        full_name=user_session['full_name'],
                        password=user_session['password']
                    )
                    login(request , registered_user)
                    code_instance.delete()
                    messages.success(request, 'You are registered!', 'success')
                elif purpose == 'login':

                    user = User.objects.filter(phone_number=phone_number).first()
                    login(request, user)
                    messages.success(request, 'You are logged in!', 'success')

                    code_instance.delete()
                    return redirect("home:home")
            else:
                messages.error(request, 'This code is wrong.', 'danger')
                return redirect("account:verify_code")
        messages.error(request, 'This code is wrong.', 'danger')
        return redirect("account:verify_code")

        
