from django.shortcuts import render
from Products.models import Products

# Create your views here.
def home_view(request):
    context = {
        'products' : Products.objects.all()
    }
    return render(request, 'home/home.html', context)
