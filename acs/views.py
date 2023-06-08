from django.shortcuts import render

from rest_framework.viewsets import ModelViewSet

from acs.models import JobApplication, JobVote
from acs.serializers import JobApplicationSerializer, JobVoteSerializer
from . models import JobPost
from . serializers import JobPostSerializer

class JobPostViewSet(ModelViewSet):
 serializer_class = JobPostSerializer
 queryset = JobPost.objects.all()
 
 
 
class JobApplicationViewSet(ModelViewSet):
 serializer_class = JobApplicationSerializer
 queryset = JobApplication.objects.all()
 

class JobVoteViewSet(ModelViewSet):
  serializer_class = JobVoteSerializer
  queryset = JobVote.objects.all()
  
  def get_serializer_context(self):
   return {
     'jobpost_id':self.kwargs['jobpost_pk'],
     'user_id': self.request.user.id,
   }