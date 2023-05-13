from django.shortcuts import render

from rest_framework.viewsets import ModelViewSet

from acs.models import JobApplication
from acs.serializers import JobApplicationSerializer
from . models import JobPost
from . serializers import JobPostSerializer

class JobPostViewSet(ModelViewSet):
 serializer_class = JobPostSerializer
 queryset = JobPost.objects.all()
 
 
 
class JobApplicationViewSet(ModelViewSet):
 serializer_class = JobApplicationSerializer
 queryset = JobApplication.objects.all()
 
