from django.shortcuts import render , get_object_or_404
from django.views import View
from .models import Product

# Create your views here.

class ProductDetailView(View):
    def get(self , request , slug):
        products = get_object_or_404(Product , slug = slug)
        return render(request , 'product/detail.html' , {'product':products})