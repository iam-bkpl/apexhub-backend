
from rest_framework import serializers

from .models import JobPost, JobApplication

from core.serializers import ExternalSerializer

class JobPostSerializer(serializers.ModelSerializer):
  # company = ExternalSerializer
  user = serializers.ReadOnlyField()
  class Meta:
    model = JobPost
    fields = ['id','user','title','company','description','date_added','is_active','salary','location','job_type','experience_level','link','expire_date']

class JobApplicationSerializer(serializers.ModelSerializer):
 class Meta:
  model = JobApplication
  fields = ['job','user','date_review', 'resume','is_active','status']
 