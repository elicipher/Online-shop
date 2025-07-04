from django.shortcuts import render
from django.views import View
from products.models import Product
from .tasks import all_bucket_object_task

# Create your views here.
class HomeView(View):
    def get(self, request):
        products = Product.objects.filter(availble = True)
        return render(request, 'home/index.html' , {'products': products})

class BucketHome(View):

    template_name = 'home/bucket.html'

    def get(self,request):
        object = all_bucket_object_task() 
        print('='*90)
        print(object)
        return render(request , self.template_name , {"objects":object})

    
