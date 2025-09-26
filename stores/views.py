from django.conf import settings
from django.urls import reverse
import requests
from rest_framework.views import APIView
from rest_framework import status,serializers
from rest_framework.response import Response

from django.shortcuts import get_object_or_404
from django.db import transaction

from .serializers import *
from . models import *



# ::::: CATEGORY ::::::
# ::: FETCH AND CREATE
class CategoryView(APIView):
    def get(self,request):
        try:
            category = Category.objects.all()
            serializer = CategorySerializer(category,many=True)
            return Response(serializer.data, status= status.HTTP_200_OK)
        except Exception as e:
            return Response({"Error":str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    def post(self,request):
        try:
            serializer = CategorySerializer(data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"Message":"Category created successfully"}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"Error":str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# ::: FETCH ,UPDATE AND DELETE
class CategoryDetailView(APIView):
    def get(self,request,id):
        try:
            category = get_object_or_404(Category, id = id)
            serializers = CategorySerializer(category)
            return Response(serializers.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"Error":str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self,request,id):
        try:
            category = get_object_or_404(Category, id = id)
            serializers = CategorySerializer(category,data=request.data,partial = True)
            if serializers.is_valid():
                serializers.save()
                return Response(serializers.data, status=status.HTTP_200_OK)
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"Error":str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def delete(self,request,id):
        try:
            category = get_object_or_404(Category, id = id)
            category.delete()
            return Response(serializers.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"Error":str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# ::::: END OF CATEGORY ::::::

# ::::: PRODUCT ::::::
# ::: FETCH AND CREATE
class ProductView(APIView):
    def get(self,request):
        try:
            product = Product.objects.all()
            serializer = ProductSerializer(product,many=True)
            return Response(serializer.data, status= status.HTTP_200_OK)
        except Exception as e:
            return Response({"Error":str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    def post(self,request):
        try:
            serializer = ProductSerializer(data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"Message":"Product created successfully"}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"Error":str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# ::: FETCH ,UPDATE AND DELETE
class ProductDetailView(APIView):
    def get(self,request,id):
        try:
            product = get_object_or_404(Product, id = id)
            serializers = ProductSerializer(product)
            return Response(serializers.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"Error":str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self,request,id):
        try:
            product = get_object_or_404(Product, id = id)
            serializers = ProductSerializer(product,data=request.data,partial = True)
            if serializers.is_valid():
                serializers.save()
                return Response(serializers.data, status=status.HTTP_200_OK)
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"Error":str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def delete(self,request,id):
        try:
            product = get_object_or_404(Product, id = id)
            product.delete()
            return Response(serializers.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"Error":str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# ::::: END OF PRODUCT ::::::

# ::::: ADD TO CART ::::::
class AddToCartView(APIView):
    def post(self,request,id):
        try:
            # get the product
            product = get_object_or_404(Product, id=id)
            # create a session cart
            cart_id = request.session.get('cart_id',None)
            # check if product is discount or actual price
            price = product.discount_price if product.discount_price else product.price

            while transaction.atomic():
                if cart_id:
                    cart = Cart.objects.filter(id=cart_id).first()

                    # assign cart to as logged in user
                    if request.user.is_authenticated and hasattr(request.user,'profile'):
                        cart.profile = request.user.profile
                        cart.save()

                    # check if cart exist
                    if cart is None:
                        cart = Cart.objects.create(total=0)
                        request.session['cart_id'] = cart.id

                    # check if product is in cart
                    this_product_in_cart = cart.cartproduct_set.filter(product=product)

                    if this_product_in_cart.exists():
                        cartproduct = this_product_in_cart.last()
                        cartproduct.quantity +=1
                        cartproduct.subtotal +=price
                        cartproduct.save()
                        cart.total +=price
                        cart.save()
                        return Response({"Message":"Item increased in cart"})
                    else:
                        cartproduct = CartProduct.objects.create(cart=cart,product=product,quantity=1,subtotal=price)
                        cartproduct.save()
                        cart.total += price
                        cart.save()
                        return Response({"Message":"New product created successfuly"})
                else:
                    cart = Cart.objects.create(total=0)
                    request.session['cart_id'] = cart.id
                    cartproduct = CartProduct.objects.create(cart=cart,product=product,quantity=1,subtotal=price)
                    cartproduct.save()
                    cart.total += price
                    cart.save()
                    return Response({"Message":"New Cart created successfuly"})
                    
        except Exception as e:
            return Response({"error":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
# ::::: END OF ADD TO CART ::::::

# ::::: MY CART ::::::
class MyCartView(APIView):
    def get(self, request):
        try:
            cart_id = request.session.get('cart_id',None)
            if cart_id:
                cart = get_object_or_404(Cart, id=cart_id)
                # assign cart to as logged in user
                if request.user.is_authenticated and hasattr(request.user,'profile'):
                    cart.profile = request.user.profile
                    cart.save()
                return Response({"Message": f'Profile - {cart.profile}'}, status=status.HTTP_200_OK)
            return Response({"Message":"Cart not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
# ::::: END OF MY CART ::::::

# ::::: MANAGE CART ::::::
class ManageCartView(APIView):
    def post(self, request, id):
        action = request.data.get('action', None)
        try:
            cart_obj = CartProduct.objects.get(id=id)
            cart = cart_obj.cart
            price = cart_obj.product.discount_price if cart_obj.product.discount_price else cart_obj.product.price

            if action == "inc":
                cart_obj.quantity += 1
                cart_obj.subtotal += price
                cart_obj.save()
                cart.total += price
                cart.save()
                return Response({"Message":"Item increase from cart"}, status=status.HTTP_200_OK)
            elif action == "dcr":
                cart_obj.quantity -= 1
                cart_obj.subtotal -= price
                cart_obj.save()
                cart.total -= price
                cart.save()
                if cart_obj.quantity == 0:
                    cart_obj.delete()
                return Response({"Message":"Item decreased from cart"}, status=status.HTTP_200_OK)
            elif action == "rmv":
                cart.total -= price
                cart.save()
                cart_obj.delete()
                return Response({"Message":"Item removed from cart"}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# ::::: END OF MANAGE CART ::::::

# ::::: CHECKOUT VIEW ::::::
class CheckoutView(APIView):
    def post(self, request):
        try:
            cart_id = request.session.get('cart_id',None)
            if cart_id is None:
                return Response({"error":"You do not have an active cart"},status=status.HTTP_400_BAD_REQUEST)
            cart_obj = get_object_or_404(Cart, id=cart_id)

            serializers = CheckOutSerializer(data=request.data)
            if serializers.is_valid():
                order = serializers.save(
                    cart = cart_obj,
                    subtotal = cart_obj.total,
                    amount = cart_obj.total
                )
                del request.session['cart_id']
                
                if order.payment_method == "paystack":
                    payment_url = reverse('payment', args=[order.id])
                    return Response({"Redirect Payment Url": payment_url}, status=status.HTTP_200_OK)
                return Response({"Message":"Order created successfully"}, status=status.HTTP_201_CREATED)
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({"error":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
# ::::: END OF CHECKOUT VIEW ::::::

# ::::: PAYMENT VIEW ::::::
class PaymentView(APIView):
    def get(self, request, id):
        try:
            order = get_object_or_404(Order, id=id)
            if order is None:
                return Response({"error":"Order not found"},status=status.HTTP_404_NOT_FOUND)
            
            url = "https://api.paystack.co/transaction/initialize" 
            headers = {"Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}"}
            data = {
                "amount": order.amount * 100, 
                "email": order.email,
                "reference": order.ref,
            }
            response = requests.post(url, data=data, headers=headers)
            response_data = response.json()

            if response_data["status"]:
                paystack_url = response_data["data"]
                return Response(
                    {
                        'order':order.id,
                        'total':order.amount,
                        'paystack_public_key':settings.PAYSTACK_PUBLIC_KEY,
                        'paystack_url':paystack_url

                    }, status=status.HTTP_200_OK
                )
            else:
                return Response({"error":"Payment initialization failed"},status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class VerifyPaymentView(APIView):
    def get(self,request,ref):
        try:
            order = get_object_or_404(Order, ref=ref)
            url = f'https://api.paystack.co/transaction/verify/{ref}'
            headers =headers = {
                "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
            }
            response = requests.get(url,headers=headers)
            response_data = response.json()

            if response_data["status"] and response_data["data"]["status"] == "success":
                order.payment_completed = True
                order.order_status = "completed"
                order.save()
                return Response({"Message": "payment was successful"}, status= status.HTTP_200_OK)
            elif response_data["data"]["status"] == "abandoned":
                order.order_status = "pending"
                order.save()
                return Response({"Message": "payment was abandoned"}, status= status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"Message":"Payment failed"}, status= status.HTTP_400_BAD_REQUEST)
        except Order.DoesNotExist:
            return Response({"Message":"Invalid payment reference"}, status= status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)