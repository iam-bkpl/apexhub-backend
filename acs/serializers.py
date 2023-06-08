
from rest_framework import serializers
from .models import JobApplication, JobPost, JobVote
from core.serializers import CustomUserSerializer, ExternalSerializer

class JobVoteSerializer(serializers.ModelSerializer):
  class Meta:
    model = JobVote
    fields = ['id','user','jobpost']
  
  # def validate(self, attrs):
  #   user = attrs['user']
  #   jobpost = attrs['jobpost']
    
  #   if JobVote.objects.filter(user=user, jobpost=jobpost).exists():
  #     raise serializers.ValidationError('You have already voted for this job post.')

  #   return attrs
  
  def create(self, validated_data):
    user_id = self.context['user_id']
    jobpost_id = self.context['jobpost_id']
    
    return JobVote.objects.create(user_id=user_id,jobpost_id=jobpost_id,**validated_data)

class JobPostSerializer(serializers.ModelSerializer):
  # company = ExternalSerializer
  # user = serializers.ReadOnlyField()

  vote_count  = JobVoteSerializer(many=True, read_only = True)
  
  class Meta:
    model = JobPost
    fields = ['id','user','title','company','description','date_added','is_active','salary','location','job_type','experience_level','link','expire_date','vote_count']

class JobApplicationSerializer(serializers.ModelSerializer):
 class Meta:
  model = JobApplication
  fields = ['job','user','date_review', 'resume','is_active','status']
 
 