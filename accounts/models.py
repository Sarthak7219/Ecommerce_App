from django.db import models
from django.contrib.auth.models import User
from base.models import BaseModel
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid
from base.emails import send_account_activation_email
from Products.models import *

class Profile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    is_email_verified = models.BooleanField()
    email_token = models.CharField(max_length=100)
    profile_img = models.ImageField(upload_to='profile')

    def get_cart_count(self):
        return CartItems.objects.filter(cart__user = self.user, cart__is_paid = False).count()
    

# @receiver(post_save, sender = User)
# def send_email_token(sender, instance, created, **kwargs):
#     try:
#         if created:
#             email_token = str(uuid.uuid4())
#             Profile.objects.create(user = instance, email_token = email_token)
#             email = instance.email
#             send_account_activation_email(email, email_token)

#     except Exception as e:
#         print(e)

class Cart(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='carts')
    is_paid = models.BooleanField(default=False)  #if is paid true that means cart items have been ordered and then the cart has to be empty.
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True, blank=True)
    razorpay_order_id = models.CharField(max_length=100, null=True, blank=True)
    razorpay_payment_id = models.CharField(max_length=100, null=True, blank=True)
    razorpay_payment_signature = models.CharField(max_length=100, null=True, blank=True)

    def get_cart_total(self):
        
        price = []
        cart_items = self.cart_items.all()
        for cart_item in cart_items:
            price.append(cart_item.product.price)

            if cart_item.color_varient:
                price.append(cart_item.color_varient.price)

            if cart_item.size_varient:
                price.append(cart_item.size_varient.price)

        if self.coupon:
            if self.coupon.min_req_amount <= sum(price):
                new_price = sum(price)-self.coupon.discount_price
                return new_price
            self.coupon = None

        return sum(price)

class CartItems(BaseModel):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey(Products, on_delete=models.SET_NULL, null=True, blank=True)
    color_varient = models.ForeignKey(ColorVarient, on_delete=models.SET_NULL, null=True, blank=True)
    size_varient = models.ForeignKey(SizeVarient, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self) -> str:
        return self.product.product_name
    
    def get_product_price(self):
        price = [self.product.price]

        if self.color_varient:
            color_varient_price = self.color_varient.price
            price.append(color_varient_price)

        if self.size_varient:
            size_varient_price = self.size_varient.price
            price.append(size_varient_price)

        return sum(price)
    