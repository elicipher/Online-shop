from django.shortcuts import render , redirect
from django.views import View
from .cart import Cart
from django.shortcuts import get_object_or_404
from products.models import Product
from .forms import CartAddForm
# Create your views here.

class CartView(View):
    def get(self,request):
        carts = Cart(request)
        return render(request , 'order/cart.html',{"cart":carts})

class CartAddView(View):

    def post(self , request , product_id):
        cart = Cart(request)
        product = get_object_or_404(Product , id=product_id)
        form = CartAddForm(request.POST)
        if form.is_valid():
            cart.add(product , form.cleaned_data['quantity'])

        
        return redirect("order:cart")
    