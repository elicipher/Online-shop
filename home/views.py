from django.shortcuts import render , redirect
from django.views import View
from products.models import Product
from . import tasks
from django.contrib import messages

# Create your views here.
class HomeView(View):
    def get(self, request):
        products = Product.objects.filter(availble = True)
        return render(request, 'home/index.html' , {'products': products})

class BucketHome(View):

    template_name = 'home/bucket.html'

    def get(self,request):
        object = tasks.all_bucket_object_task() 
        print('='*90)
        print(object)
        return render(request , self.template_name , {"objects":object})

class DeleteBucketObject(View):
    def get(self, request , key ):
        tasks.delete_object_task.delay(key)
        messages.success(request , "we will delete your object soon .","info")
        return redirect("home:bucket_home")

    
