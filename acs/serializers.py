
from rest_framework import serializers

from .models import JobPost, JobApplication

class JobPostSerializer(serializers.ModelSerializer):
 class Meta:
  model = JobPost
  fields = ['company_name','title','description','date_added','is_active','salary','location','job_type','experience_level','link','expire_date']

class JobApplicationSerializer(serializers.ModelSerializer):
 class Meta:
  model = JobApplication
  fields = ['job','user','date_review', 'resume','is_active','status']
 