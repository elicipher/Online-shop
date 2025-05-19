from django.urls import path
from . import views

app_name = 'account'
urlpatterns = [
    path('register/',views.UserRegisterView.as_view(), name='user_register'),
    path('verfy/',views.VerfyCodeView.as_view(), name='verfy_code'),
    path('login/',views.LoginView.as_view(), name='user_login'),
    path('logout/',views.LogoutView.as_view(), name='user_logout'),
]