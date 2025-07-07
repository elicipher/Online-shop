from django.shortcuts import render , redirect
from django.views import View 
from products.forms import UploadObjectForm
from products.models import Product
from products.forms import UploadObjectForm
from . import tasks
from django.contrib import messages
from django.core.files.storage import default_storage
import os
from django.conf import settings
from django.contrib.auth.mixins import UserPassesTestMixin

# Create your views here.
class HomeView(View):
    def get(self, request):
        products = Product.objects.filter(availble = True)
        return render(request, 'home/index.html' , {'products': products})

class BucketHome(UserPassesTestMixin , View):

    template_name = 'home/bucket.html'
    form_class = UploadObjectForm

    def get(self,request):
        form = self.form_class()
        object = tasks.all_bucket_object_task() 
        return render(request , self.template_name , {"objects":object , "form":form})
    #واسه محدود کردن کاربران به دسترسی باکت ها
    #فقط کاربرانی که لاگین کردن و ادمین هستن
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_admin
    
class DeleteBucketObject(UserPassesTestMixin,View):
    def get(self, request , key ):
        tasks.delete_object_task.delay(key)
        messages.success(request , "we will delete your object soon .","info")
        return redirect("home:bucket_home")

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_admin

    
class DownloadBucketObject(UserPassesTestMixin, View):

    def get(self,request , key):
        tasks.download_object_task.delay(key)
        messages.success(request , "we will download your object soon .","info")
        return redirect("home:bucket_home")

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_admin


class UploadBucketObject(UserPassesTestMixin ,View):
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

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_admin
