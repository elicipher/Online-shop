from django.urls import path
from . import views

app_name = 'account'
urlpatterns = [
    path('register/',views.UserRegisterView.as_view(), name='user_register'),
    path('verfy/',views.VerfyCodeRegistrationView.as_view(), name='verfy_code'),
]