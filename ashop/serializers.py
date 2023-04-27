import django.db
from rest_framework import serializers
from . models import Category,Product


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','title','product_count']
        
    
    product_count = serializers.IntegerField(read_only=True)