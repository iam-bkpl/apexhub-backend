from rest_framework.response import Response
from ashop.models import Category, Product, ProductImage
from rest_framework.generics import ListCreateAPIView
from rest_framework.viewsets import ModelViewSet
from ashop.serializers import CollectionSerializer, ProductImageSerializer, ProductSerializer

class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CollectionSerializer
    # def get_queryset(self):
    #     return Category.objects.all()
    
    # def get_serializer_class(self):
    #     return CollectionSerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.prefetch_related('images').all()
    serializer_class = ProductSerializer
    
    
class ProductImageViewSet(ModelViewSet):
    serializer_class = ProductImageSerializer
    queryset = ProductImage.objects.all()