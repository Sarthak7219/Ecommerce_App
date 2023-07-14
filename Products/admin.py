from django.contrib import admin
from .models import *


admin.site.register(Category)

admin.site.register(Coupon)

class ProductImageAdmin(admin.StackedInline):
    model = ProductImage

class ProductAdmin(admin.ModelAdmin):
    list_display = ['product_name', 'price']
    inlines = [ProductImageAdmin]

@admin.register(ColorVarient)
class ColorVarientAdmin(admin.ModelAdmin):
    model = ColorVarient
    list_display = ['color_varient', 'price']

@admin.register(SizeVarient)
class SizeVarientAdmin(admin.ModelAdmin):
    model = SizeVarient
    list_display = ['size_varient', 'price']
    


admin.site.register(Products, ProductAdmin)

admin.site.register(ProductImage) 


