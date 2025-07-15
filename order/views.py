from django.shortcuts import render , redirect
from django.views import View
from .cart import Cart
from django.shortcuts import get_object_or_404
from products.models import Product
from .forms import CartAddForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Order , OrderItem
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
    

class CartRemoveView(View):
    def get(self , request , product_id):
        cart = Cart(request)
        product = get_object_or_404(Product , id=product_id)
        cart.remove(product)
        return redirect("order:cart")

class OrderCreateView(LoginRequiredMixin ,View):
    def get(self , request):
        cart = Cart(request)
        order = Order.objects.create(user=request.user)
        for item in cart :
            OrderItem.objects.create(order = order , product=item['product'],price=item['price'],quantity=item['quantity'])
        cart.clear()
        return redirect("order:order_detail",order.id)


class OrderDetailView(LoginRequiredMixin,View):
    def get(self , request , order_id ):
        order = get_object_or_404(Order , id = order_id)
        return render(request , "order/order.html",{"order":order})