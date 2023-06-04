import django.shortcuts
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db.models.aggregates import Count
from ashop.serializers import (CollectionSerializer, CommentSerialier, OrderSerializer,
    ProductImageSerializer, ProductSerializer, RatingSerializer)
from ashop.models import Cart, Category, Order, Product, ProductImage, Rating,Comment
from rest_framework.viewsets import ModelViewSet
from core.models import CustomUser


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

    def get_serializer_context(self):
        return {'product_id':self.kwargs['product_pk']}


class RatingViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        return RatingSerializer
    
    def get_queryset(self):
        return Rating.objects.filter(product_id=self.kwargs['product_pk'])

    def get_serializer_context(self):
        return {
            'product_id':self.kwargs['product_pk'],
            'user_id':self.request.user.id
        }


class CommentViewSet(ModelViewSet):
    permission_classes=[IsAuthenticated]
    
    def get_serializer_class(self):
        return CommentSerialier
    
    def get_queryset(self):
        return Comment.objects.filter(product_id = self.kwargs['product_pk'])

    def get_serializer_context(self):
        return {
            'product_id': self.kwargs['product_pk'],
            'user_id' : self.request.user.id,
                }

class OrderViewSet(ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        
        if user.is_admin:
            return Order.objects.all()

        elif user.user_type =='student':
            (student_id,created) = CustomUser.objects.only('id').get_or_create(id=user.id)
            return Order.objects.filter(user_id = student_id)
        else:
            return None


class EsewaViewSet(ModelViewSet):
    def get(self,request,*args, **kwargs):
        pass
    
    def post(self,*args, **kwargs):
        pass
    