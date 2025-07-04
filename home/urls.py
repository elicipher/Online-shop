from django.urls import path
from .views import HomeView , BucketHome , DeleteBucketObject

app_name ='home'
urlpatterns =[
    path('',HomeView.as_view(),name='home'),
    path('bucket/', BucketHome.as_view(),name="bucket_home"),
    path("delet_obj/<path:key>/",DeleteBucketObject.as_view(), name="delete_bucket_obj")
]