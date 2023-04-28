from rest_framework import serializers
from ashop.models import Product
from . models import Category,Product


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','title','product_count']
        
    product_count = serializers.IntegerField(read_only=True)
    
    
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model : Product
        fields = ['id','name','slug','description','price','stock','date_added','date_update']