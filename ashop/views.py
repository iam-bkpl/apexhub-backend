from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView
from django.db.models.aggregates import Count
from ashop.serializers import (CollectionSerializer, CommentSerialier,
    OrderItemSerializer, PaymentSerializer, ProductImageSerializer, ProductSerializer,
    RatingSerializer)
from ashop.models import Category, Comment, OrderItem, Payment, Product, ProductImage, Rating
from rest_framework.viewsets import ModelViewSet
from core.models import CustomUser
from django_filters.rest_framework import DjangoFilterBackend
import rest_framework
from rest_framework.filters import SearchFilter, OrderingFilter
from .filter import CategoryFilter

class CategoryViewSet(ModelViewSet):
    serializer_class = CollectionSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['name']
    # filterset_class = CategoryFilter
    # search_fields = ['name','product_set__name']
    
    def get_queryset(self):
        return Category.objects.annotate(
            products_count = Count('products')).all()
    
    def get_serializer_class(self):
        return CollectionSerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.prefetch_related('images').all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter,OrderingFilter]
    # filterset_fields = ['name', 'seller', 'category']
    search_fields = ['name','category__name']
    ordering_fields = ['price', 'date_updated','date_added']
    def get_serializer_context(self):
        return {'request': self.request}
    
class ProductImageViewSet(ModelViewSet):
    serializer_class = ProductImageSerializer
    queryset = ProductImage.objects.all()

    def get_serializer_context(self):
        return {  
            'product_id':self.kwargs['product_pk']
            }


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


class OrderItemViewSet(ModelViewSet):
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        
        if user.is_admin:
            return OrderItem.objects.all()

        elif user.user_type =='student':
            (student_id,created) = CustomUser.objects.only('id').get_or_create(id=user.id)
            return OrderItem.objects.filter(buyer_id = student_id)
        else:
            return None
        
    # def get_serializer_class(self):
    #     if self.request.method == 'POST':
    #         return OrderItemSerializer
        
    #     elif self.request.method == 'GET':
    #         return GetOrderSerializer
        
        
    def get_serializer_context(self):
        return {
            'buyer_id':self.request.user.id,
            'product_id':self.kwargs['product_pk']
                }



class PaymentViewSet(ModelViewSet):
    serializer_class = PaymentSerializer    
    permission_classes =[IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        
        if user.is_admin:
            return Payment.objects.all()

        elif user.user_type =='student':
            (student_id, created) = CustomUser.objects.only('id').get_or_create(id=user.id)
            return Payment.objects.filter(buyer_id = student_id)
        else:
            return None
                 
                 
    def get_serializer_context(self):
        return {
            'buyer_id':self.request.user.id,
            'order_id':self.kwargs['order_pk']
            }