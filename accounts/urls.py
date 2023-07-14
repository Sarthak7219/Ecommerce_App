from django.contrib import admin
from django.urls import path
from .views import *


urlpatterns = [
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('add-to-cart/<uid>/', add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<uid>/', remove_from_cart, name='remove-from-cart'),
    path('cart/', cart_view, name='cart'),
    path('remove-coupon/<cart_uid>/', remove_coupon, name='remove-coupon'),
    path('payment-success/', payment_success, name='payment-success')
]
