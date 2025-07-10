from django.shortcuts import render , redirect
from django.views import View 
from products.forms import UploadObjectForm
from products.models import Product ,Category
from products.forms import UploadObjectForm
from . import tasks
from django.contrib import messages
from django.core.files.storage import default_storage
import os
from django.conf import settings
from utils import IsAdminUserMixin

# Create your views here.
class HomeView(View):
    def get(self, request , category_slug=None):
        products = Product.objects.filter(availble = True)
        categories = Category.objects.filter(is_sub=False)
        if category_slug :
            category = Category.objects.get(slug=category_slug)
            products = products.filter(category=category)
        return render(request, 'home/index.html' , {'products': products , 'categories':categories})

class BucketHome(IsAdminUserMixin , View):

    template_name = 'home/bucket.html'
    form_class = UploadObjectForm

    def get(self,request):
        form = self.form_class()
        object = tasks.all_bucket_object_task() 
        return render(request , self.template_name , {"objects":object , "form":form})

   
    
class DeleteBucketObject(IsAdminUserMixin,View):
    def get(self, request , key ):
        tasks.delete_object_task.delay(key)
        messages.success(request , "we will delete your object soon .","info")
        return redirect("home:bucket_home")

   

    
class DownloadBucketObject(IsAdminUserMixin, View):

    def get(self,request , key):
        tasks.download_object_task.delay(key)
        messages.success(request , "we will download your object soon .","info")
        return redirect("home:bucket_home")

   


class UploadBucketObject(IsAdminUserMixin ,View):
    form_class = UploadObjectForm

    def post(self, request):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            cd = form.cleaned_data
            image = cd.get("img")
            temp_path = os.path.join(settings.MEDIA_ROOT, "temp_uploads", image.name)
            default_storage.save("temp_uploads/" + image.name, image)
            tasks.upload_object_task.delay(temp_path)

            messages.success(request, "We will upload your object soon.", "info")
            return redirect("home:bucket_home")

        messages.error(request, "Failed.", "danger")
        return redirect("home:bucket_home")

   
