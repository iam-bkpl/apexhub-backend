from django.contrib import admin
from .models import (Category, Comment, Order, OrderItem, Product, ProductImage,
    Rating)


class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields ={
        'slug':['name']
    }
    
admin.site.register(Category)
admin.site.register(Product,ProductAdmin)
admin.site.register(ProductImage)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Rating)
admin.site.register(Comment)
# admin.site.register(Cart)
# admin.site.register(CartItem)


