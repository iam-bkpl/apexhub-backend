from django.contrib import admin
from .models import (Category, Comment, OrderItem, Product, ProductImage,Payment,
    Rating)


class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields ={
        'slug':['name']
    }
    list_display = ['name','seller','price','stock']

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['id','buyer','product_id','product','payment_status']
    
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['buyer','order','date','payment_method','amount']
    
    
admin.site.register(Category)
admin.site.register(Product,ProductAdmin)
admin.site.register(ProductImage)
admin.site.register(OrderItem,OrderItemAdmin)
admin.site.register(Payment,PaymentAdmin )
admin.site.register(Rating)
admin.site.register(Comment)
# admin.site.register(Cart)
# admin.site.register(CartItem)


