from django.db import models
from apexhub.settings import AUTH_USER_MODEL
from django.conf import settings

class Category(models.Model):
    name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name
    

class Product(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    stock = models.IntegerField()
    date_added = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    date_update = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='products')

    
class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(
        upload_to='product/images')
    

class Order(models.Model):
    PAYMENT_STATUS_PENDING = 'P'
    PAYMENT_STATUS_COMPLETE = 'C'
    PAYMENT_STATUS_FAILED = 'F'
    PAYMENT_STATUS_CHOICES = [
        (PAYMENT_STATUS_PENDING, 'Pending'),
        (PAYMENT_STATUS_COMPLETE, 'Complete'),
        (PAYMENT_STATUS_FAILED, 'Failed')
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    date_placed = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=1,
                                      choices=PAYMENT_STATUS_CHOICES,
                                      default=PAYMENT_STATUS_PENDING)
    
    
class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.PROTECT,
        related_name='items'
    )
    product = models.ForeignKey(Product,
                                on_delete=models.PROTECT,
                                related_name='orderitems')
    quantity = models.PositiveSmallIntegerField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    

