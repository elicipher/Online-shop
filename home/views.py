from django.shortcuts import render
from django.views import View
from products.models import Product

# Create your views here.
class HomeView(View):
    def get(self, request):
        products = Product.objects.filter(availble = True)
        return render(request, 'home/index.html' , {'products': products})
    

    
