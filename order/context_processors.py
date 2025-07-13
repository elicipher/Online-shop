from .cart import Cart

def cart(request):
    return {"items_In_Cart": Cart(request)}