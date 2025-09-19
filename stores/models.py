from django.db import models

from users.models import Profile

import secrets

class Category(models.Model):
    title = models.CharField(max_length=50)
    image = models.ImageField(upload_to='stores/category')
    crated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Product(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    price = models.BigIntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    discount_price = models.BigIntegerField(null=True,blank=True)
    image = models.ImageField(upload_to='stores/products')
    photo1 = models.ImageField(upload_to='stores/products',null=True,blank=True)
    photo2 = models.ImageField(upload_to='stores/products',null=True,blank=True)
    photo3 = models.ImageField(upload_to='stores/products',null=True,blank=True)
    photo4 = models.ImageField(upload_to='stores/products',null=True,blank=True)
    photo5 = models.ImageField(upload_to='stores/products',null=True,blank=True)
    rating = models.IntegerField(default=0)
    reviews = models.TextField()
    color = models.CharField(max_length=50,null=True,blank=True)
    size = models.CharField(max_length=50,null=True,blank=True)
    length = models.CharField(max_length=50,null=True,blank=True)
    ingredient = models.CharField(max_length=50,null=True,blank=True)
    in_stock = models.IntegerField(default=0)
    is_available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.title

# cart
class Cart(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
    total = models.PositiveBigIntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Cart - {self.total}'

# cartproduct
class CartProduct(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.BigIntegerField()
    subtotal = models.BigIntegerField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'CartId -{self.cart.id} <===> {self.quantity}'

# order
ORDER_STATUS=(
    ('pending','pending'),
    ('completed','completed'),
    ('canceled','canceled'),
)
PAYMENT_METHOD=(
    ('paystack','paystack'),
    ('paypal','paypal'),
    ('fluter','fluter'),
)
class Order():
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    order_by = models.CharField(max_length=255)
    shipping_address = models.TextField()
    mobile = models.CharField(max_length=50)
    email = models.EmailField()
    subtotal = models.BigIntegerField()
    amount = models.BigIntegerField()
    order_status = models.CharField(default='pending', choices=ORDER_STATUS)
    payment_method = models.CharField(default='paystack', choices=PAYMENT_METHOD)
    payment_completed = models.BooleanField(default = False)
    ref = models.CharField(max_length=255, unique=True, null=True, blank=True)

    def __str__(self):
        return f'OrderId-{self.id} = {self.amount}'
    
    def save(self,*args, **kwargs):
        while not self.ref:
            ref = secrets.token_urlsafe(50)
            obj_with_sm_ref = Order.objects.filter(ref=ref)
            if not obj_with_sm_ref:
                self.ref = ref
        super().save(*args,**kwargs)

    def amount_value(self)->int:
        self.amount * 100

    # verify
