from django.urls import path , include
from .views import HomeView , BucketHome , DeleteBucketObject ,DownloadBucketObject, UploadBucketObject


app_name ='home'
bucket_urls = [

    path('', BucketHome.as_view(),name="bucket_home"),
    path("delete_obj/<path:key>/",DeleteBucketObject.as_view(), name="delete_bucket_obj"),
    path('download_obj/<path:key>',DownloadBucketObject.as_view(),name="download_bucket_obj"),
    path("upload_obj/",UploadBucketObject.as_view(),name= "upload_bucket_obj")
  

]

urlpatterns =[
    path('',HomeView.as_view(),name='home'),
    path('categoty/<slug:category_slug>/',HomeView.as_view(),name='categoty_url'),
    path('bucket/',include(bucket_urls))

    
]