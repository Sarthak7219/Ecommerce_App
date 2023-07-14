from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from accounts.models import Cart,CartItems,Profile
from Products.models import *
import razorpay
from django.conf import settings


# Create your views here.
def login_view(request):
    if request.method == "POST":
        username = request.POST.get('email')
        password = request.POST.get('password')

        user_obj = authenticate(request, username = username, password = password)

        if user_obj is None:
            messages.warning(request, "Invalid username or password")
            return HttpResponseRedirect(request.path_info)
        
        # if not user_obj.profile.is_email_verified:
        #     messages.warning(request, "Account is not verified")
        #     return HttpResponseRedirect(request.path_info)

        login(request,user_obj)
        return redirect('/')
        
    return render(request, "accounts/login.html")

def register_view(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        user_obj = User.objects.filter(username = email)

        if user_obj.exists() :
            messages.warning(request, "Email is already registered ")
            return HttpResponseRedirect(request.path_info)
        
        user_obj = User.objects.create(
            first_name = first_name,
            last_name = last_name,
            email = email,
            username = email
        )
        user_obj.set_password(password)
        user_obj.save()
        

        
        
        messages.success(request, "A verification email has been sent to your mail")
        return HttpResponseRedirect(request.path_info)


    return render(request, 'accounts/register.html')


def add_to_cart(request, uid):
    product = Products.objects.get(uid = uid)
    user = request.user
    varient = request.GET.get('varient')
    cart , _ = Cart.objects.get_or_create(user = user, is_paid = False)
    cart_item = CartItems.objects.create(cart = cart, product = product)
    messages.success(request, "Item added to your cart successfully!")

    

    if varient:
        varient = request.GET.get('varient')
        size_varient = SizeVarient.objects.get(size_varient = varient)
        cart_item.size_varient = size_varient
        cart_item.save()
        
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def remove_from_cart(request, uid):
    try:
        cart_item = CartItems.objects.get(uid = uid)
        cart_item.delete()

    except Exception as e:
        print(e)
    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



def cart_view(request):
    try:
        cart = Cart.objects.get(is_paid = False, user = request.user)

    except Exception as e:
        print(e)
    cart_items = CartItems.objects.filter(cart = cart)

    

    if request.POST:
        coupon = request.POST.get('coupon')
        coupon_obj = Coupon.objects.filter(coupon_code__icontains = coupon)
        if not coupon_obj :    
            messages.warning(request, "Invalid Coupon!")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
        if cart.get_cart_total() < coupon_obj[0].min_req_amount:
            messages.warning(request, f'Minimum amount should be {coupon_obj[0].min_req_amount}')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
        if coupon_obj[0].is_expired:
            messages.warning(request, 'Coupon expired!')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
        if cart.coupon:
            messages.warning(request, 'Coupon already exists!')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        cart.coupon = coupon_obj[0]

        cart.save()
        messages.success(request, "Coupon applied successfully!")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    

    #Razorpay
    client = razorpay.Client(auth= (settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
    payment = client.order.create({'amount' : cart.get_cart_total()*100, 'currency' : 'INR', 'payment_capture' : 1})
    print(payment)
    cart.razorpay_order_id = payment['id']
    cart.save()

    context = {
        'cart' : cart,
        'cart_items' : cart_items,
        'payment' : payment
        
    }

    return render(request, 'accounts/cart.html', context)

def remove_coupon(request, cart_uid):
    cart = Cart.objects.get(uid = cart_uid)
    cart.coupon = None
    cart.save()
    messages.success(request, "Coupon removed!")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    

def payment_success(request):
    razorpay_order_id = request.GET.get('razorpay_order_id')
    cart = Cart.objects.get(razorpay_order_id = razorpay_order_id)
    cart.is_paid = True
    cart.save()
    return HttpResponse("Payment Succesful!")
    
    







