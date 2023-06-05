import django.db
from rest_framework import serializers
from ashop.models import Cart, Category, Comment, Order, OrderItem, Product, ProductImage, Rating


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


class RatingSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only=True)
    class Meta:
        model = Rating
        fields = ['id','rate', 'user_id','date_added']
    
    def create(self, validated_data):
        product_id = self.context['product_id']
        user_id = self.context['user_id']
        return Rating.objects.create(product_id=product_id,user_id=user_id, **validated_data)
    
    
class CommentSerialier(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only = True)
    class Meta:
        model = Comment
        fields = ['id','user_id','text','date_added']
        
    def create(self, validated_data):
        return Comment.objects.create(
            user_id=self.context['user_id'],
            product_id=self.context['product_id'],
            **validated_data
            )
        
class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only = True)
    ratings = RatingSerializer(many=True, read_only = True)
    comments = CommentSerialier(many=True, read_only=True)
    
    class Meta:
        model = Product
        fields = ['id','name','slug','description','price','stock','date_added','is_active','category','images','ratings','comments']
        
class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id','name','price']
    
    
class OrderItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer()
    class Meta:
        model = OrderItem
        fields = ['id','product','quantity','price']
        

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    class Meta:
        model = Order
        fields = ['id','user','payment_status','items','date_placed']




        
# class CartSerializer(serializers.ModelSerializer):
#     # id =  serializers.IntegerField()
#     class Meta:
#         model = Cart
#         fields = ['id','items','total_price']

