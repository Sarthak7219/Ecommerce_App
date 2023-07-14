from django.shortcuts import render
from .models import *
from django.http import HttpResponseRedirect


# Create your views here.
def product_detail_view(request, slug):
    try : 
        product = Products.objects.get(slug = slug)
        context = {
            'product' : product,
        }
        if request.GET.get('size'):
            size = request.GET.get('size')
            price = product.get_product_price_by_size(size)
            context['selected_size'] = size 
            context['updated_price'] = price

        return render(request, 'product/product.html', context)
    
    except Exception as e:
        print(e)





    
