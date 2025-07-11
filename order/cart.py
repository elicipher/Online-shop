CART_SESSION_ID = 'cart'

class Cart:
    def __init__(self , request):
        self.session = request.session
        cart = self.session.get(CART_SESSION_ID)

        #اگه سشن نداشت براش بساز و مقدارش رو یک دیکشنری خالی بزار
        if not cart :
            cart = self.session[CART_SESSION_ID] = {}
        self.cart = cart


