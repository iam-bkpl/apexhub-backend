from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin, RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from core.models import Acs, External, Student
from .serializers import AcsSerializer, ExternalSerializer, StudentSerializer


class StudentViewSet(CreateModelMixin,UpdateModelMixin,RetrieveModelMixin,GenericViewSet):
#  queryset = Student.objects.all()
 serializer_class = StudentSerializer
 
 def get_queryset(self):
    return  Student.objects.all()
 
 
class ExternalViewSet(CreateModelMixin,RetrieveModelMixin,UpdateModelMixin, GenericViewSet):
 queryset = External.objects.all()
 serializer_class = ExternalSerializer
 
 
class AcsViewSet(ModelViewSet):
 queryset = Acs.objects.all()
 serializer_class = AcsSerializer