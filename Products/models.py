from django.db import models
from base.models import BaseModel
from django.utils.text import slugify
# Create your models here.

class Category(BaseModel):

    category_name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, null=True, blank=True)
    category_image = models.ImageField(upload_to="categories")

    def save(self, *args, **kwargs):
        self.slug = slugify(self.category_name)
        super(Category, self).save(*args, **kwargs)

    def __str__(self) -> str:    #to display name of category in the admin panel
        return self.category_name
    
class ColorVarient(BaseModel):
    color_varient = models.CharField(max_length=100, blank=True)
    price = models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.color_varient

class SizeVarient(BaseModel):
    size_varient = models.CharField(max_length=50, blank=True)
    price = models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.size_varient

class Products(BaseModel):

    product_name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")
    # In the example above, the Book model has a foreign key relationship to the Author model, and the related_name parameter is set to 'books'. This means that you can access the set of books written by an author using the books attribute on an Author object:
    price = models.IntegerField()
    product_description = models.TextField()
    color_varient = models.ManyToManyField(ColorVarient)
    size_varient = models.ManyToManyField(SizeVarient)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.product_name)
        super(Products, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.product_name
    
    def get_product_price_by_size(self, size):
        return self.price + SizeVarient.objects.get(size_varient = size).price

class ProductImage(BaseModel):
    products = models.ForeignKey(Products, on_delete=models.CASCADE, related_name="product_images")
    image = models.ImageField(upload_to="products")


class Coupon(BaseModel):
    coupon_code = models.CharField(max_length=10)
    is_expired = models.BooleanField(default=False)
    discount_price = models.IntegerField(default=100)
    min_req_amount = models.IntegerField(default=500)

    def __str__(self) -> str:
        return self.coupon_code
