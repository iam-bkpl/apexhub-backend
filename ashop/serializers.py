from rest_framework import serializers
from ashop.models import Category, Product, ProductImage
from . models import Category,Product


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','name','products_count']
        
    products_count = serializers.IntegerField(read_only=True)
    
class ProductImageSerializer(serializers.ModelSerializer):
 
    
    def create(self, validated_data):
        product_id = self.context['product_id']
        return ProductImage.objects.create(product_id=product_id, **validated_data)
    
    class Meta:
        model = ProductImage
        fields = ['id','image']
    
class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only = True)
    class Meta:
        model = Product
        fields = ['id','name','slug','description','price','stock','date_added','is_active','category','images']