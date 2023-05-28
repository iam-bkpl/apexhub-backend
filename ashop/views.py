from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db.models.aggregates import Count
from ashop.serializers import CollectionSerializer, ProductImageSerializer, ProductSerializer
from ashop.models import Category, Product, ProductImage


class CategoryViewSet(ModelViewSet):
    serializer_class = CollectionSerializer
    
    def get_queryset(self):
        return Category.objects.annotate(
            products_count = Count('products')).all()
    
    # def get_serializer_class(self):
    #     return CollectionSerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.prefetch_related('images').all()
    serializer_class = ProductSerializer
    search_fields =['name','description']

    def get_serializer_context(self):
        return {'request': self.request}

    
    
    
class ProductImageViewSet(ModelViewSet):
    serializer_class = ProductImageSerializer
    queryset = ProductImage.objects.all()