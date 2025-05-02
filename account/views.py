from django.shortcuts import render
from django.views import View
from .forms import UserRegitrationForm
# Create your views here.

class UserRegisterView(View):
    form_class = UserRegitrationForm

    def get(self , request):
        form = self.UserRegitrationForm()
        return render(request , 'regiseter.html', {'form':form})

    def post(self , request):
        pass
