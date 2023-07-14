from django.urls import path
from .views import product_detail_view


urlpatterns = [
    path('<slug>/', product_detail_view, name='product_detail'),
    
]