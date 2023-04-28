from rest_framework.response import Response
from ashop.models import Category, Product
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView
from ashop.serializers import CollectionSerializer

class CategoryView(ListCreateAPIView):
    def get_queryset(self):
        return Category.objects.all()
    
    def get_serializer_class(self):
        return CollectionSerializer

    

