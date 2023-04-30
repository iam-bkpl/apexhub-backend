import django.db
from rest_framework import serializers
from ashop.models import Category, Product
from . models import Category,Product


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','name','product_count']
        
    product_count = serializers.IntegerField(read_only=True)
    
    
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id','name','slug','description','price','stock','date_added','is_active','category']