from django.db.models import Count
from rest_framework import serializers
from .models import JobApplication, JobPost, JobVote
from core.serializers import CustomUserSerializer, ExternalSerializer
from rest_framework.response import Response

class JobVoteSerializer(serializers.ModelSerializer):
  class Meta:
    model = JobVote
    fields = ['id','user','jobpost']

  def validate(self, attrs):
    user = attrs['user']
    jobpost = attrs['jobpost']
    print("validate function ")
    
    # try:
    #   job_vote = JobVote.objects.filter(user=user, jobpost=jobpost)
    #   job_vote.delete()
    #   raise serializers.ValidationError('job vote deleted')
    
    # except JobVote.DoesNotExist:
    #   return attrs
    
    # try:
    #         job_vote = JobVote.objects.get(user=user, jobpost=jobpost)
    #         if self.instance and self.instance.pk == job_vote.pk:
    #             # Ignore the existing vote if it belongs to the same instance being updated
    #             pass
    #         else:
    #             job_vote.delete()
    # except JobVote.DoesNotExist:
    #         pass
    
    if JobVote.objects.filter(user=user, jobpost=jobpost).exists():
      print("job post exist")
      JobVote.objects.filter(user=user, jobpost=jobpost).delete()
      raise serializers.ValidationError({'detail':'job vote deleted'})
    else:
      print('job voote does not exist')
      return attrs

  
  # def create(self, validated_data):
  #   user_id = self.context['user_id']
  #   jobpost_id = self.context['jobpost_id']
    
  #   return JobVote.objects.create(user_id=user_id,jobpost_id=jobpost_id,**validated_data)

class JobPostSerializer(serializers.ModelSerializer):
  # company = ExternalSerializer
  # user = serializers.ReadOnlyField()

  vote_count = serializers.SerializerMethodField()
  
  def get_vote_count(self, job_post):
    return job_post.jobvote_set.count()
  
  class Meta:
    model = JobPost
    fields = ['id','title','company','vacancy','description','date_added','is_active','salary','location','job_type','experience_level','link','expire_date','vote_count']

  def create(self, validated_data):
    user = self.context['user']
    return JobPost.objects.create(user=user, **validated_data)


class JobApplicationSerializer(serializers.ModelSerializer):
 class Meta:
  model = JobApplication
  fields = ['job','user','date_review', 'resume','is_active','status']
 
 