from products.models import Product

CART_SESSION_ID = 'cart'

class Cart:
    def __init__(self , request):
        self.session = request.session
        cart = self.session.get(CART_SESSION_ID)

        #اگه سشن نداشت براش بساز و مقدارش رو یک دیکشنری خالی بزار
        if not cart :
            cart = self.session[CART_SESSION_ID] = {}
        self.cart = cart
    
    def __iter__(self ):
        product_id = self.cart.keys() # آیدی محصولاتمو میگیرم - بهمون لیستی از آیدی ها رو برمیگردونه
        products = Product.objects.filter(id__in =product_id ) #id__in چون لیست رو داریم نگاه میکنیم ازین استفاده میکنیم
        cart = self.cart.copy()
        for product in products:
            self.cart[str(product.id)]['product'] = product #یا product.name

        for item in self.cart.values() :
            item["total_price"] = int(item['price']) * item['quantity']
            yield item




    def add(self,product ,quantity):
        product_id = str(product.id)
        if product_id not in self.cart :#اگر در سبد خرید نبود
            self.cart[product_id]={'quantity':0,'price':str(product.price)}
            # price استرینگ کردیم چون ‍‍جی سان نمیتونه ذخیرش کنه 
        self.cart[product_id]['quantity'] += quantity
        self.save()

    def remove(self , product):
        product_id = str(product.id)
        if product_id in self.cart :
            del self.cart[product_id]
            self.save()

    def save(self):

        self.session.modified = True


    def get_total_price(self):
        return sum(int(item['price']) * item['quantity'] for item in self.cart.values())



