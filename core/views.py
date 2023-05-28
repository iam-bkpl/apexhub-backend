from django.shortcuts import render
import rest_framework
from rest_framework.response import Response
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin, RetrieveModelMixin
from rest_framework.decorators import action
import rest_framework.routers
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from core.models import Acs, External, Student
from .serializers import AcsSerializer, ExternalSerializer, StudentSerializer


class StudentViewSet(CreateModelMixin,UpdateModelMixin,RetrieveModelMixin,GenericViewSet):
 serializer_class = StudentSerializer
 queryset = Student.objects.all()
 
 @action(detail=False,methods=['GET','PUT'])
 def me(self,request):
     (student,created) = Student.objects.get_or_create(
         user_id = request.user.id
     )
     if request.method == 'GET':
         serializers = StudentSerializer(student)
         return Response(serializers.data)
     elif request.method == 'PUT':
         serializers = StudentSerializer(student,
         data = request.data)
         serializers.is_valid(raise_exception=True)
         serializers.save()
         return Response(serializers.data)
         
 
class ExternalViewSet(CreateModelMixin,RetrieveModelMixin,UpdateModelMixin, GenericViewSet):
 queryset = External.objects.all()
 serializer_class = ExternalSerializer

 @action(detail=True, methods=['GET','PUT'])
 def me(self,request):
     pass
     
 
 
class AcsViewSet(ModelViewSet):
 queryset = Acs.objects.all()
 serializer_class = AcsSerializer