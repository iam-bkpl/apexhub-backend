
from rest_framework.viewsets import ModelViewSet
from acs.models import JobApplication, JobVote
from acs.serializers import JobApplicationSerializer, JobVoteSerializer
from . models import JobPost
from . serializers import JobPostSerializer
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter


class JobPostViewSet(ModelViewSet):
 serializer_class = JobPostSerializer
 queryset = JobPost.objects.all()
 filter_backends = [DjangoFilterBackend,SearchFilter,OrderingFilter]
 search_fields = ['company','title','description','experience_level','location']
 ordering_fields = ['date_added','salary','date_updated','expire_date']
 
class JobApplicationViewSet(ModelViewSet):
 serializer_class = JobApplicationSerializer
 queryset = JobApplication.objects.all()
 filter_backends = [DjangoFilterBackend, SearchFilter,OrderingFilter]
 search_fields = ['user']
 ordering_fields = ['date_applied','date_review']
 filterset_fields = ['user','status']
 
 def get_queryset(self):
  user = self.request.user
  
  if user.is_staff:
     return JobApplication.objects.all()
  return JobApplication.objects.filter(user=user)

class JobVoteViewSet(ModelViewSet):
  serializer_class = JobVoteSerializer
  queryset = JobVote.objects.all()
  
  def get_serializer_context(self):
   return {
     'jobpost_id':self.kwargs['jobpost_pk'],
     'user_id': self.request.user.id,
   }
   
   
  def get_queryset(self):
   return JobVote.objects.filter(jobpost = self.kwargs['jobpost_pk'])