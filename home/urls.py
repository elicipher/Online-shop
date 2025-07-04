from django.urls import path
from .views import HomeView , BucketHome

app_name ='home'
urlpatterns =[
    path('',HomeView.as_view(),name='home'),
    path('bucket/', BucketHome.as_view(),name="bucket_home"),
]