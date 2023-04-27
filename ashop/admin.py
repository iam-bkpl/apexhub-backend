from django.contrib import admin
from .models import (Cart, CartItem, Category, Comment, Order, OrderItem, Product, ProductImage,
    Rating)

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Rating)
admin.site.register(Comment)
admin.site.register(Cart)
admin.site.register(CartItem)


