from django.db import models
from django.conf import settings
from apexhub.settings import AUTH_USER_MODEL
from core.models import CustomUser

    # job type 
    
JOB_TYPE_REMOTE = 'remote'
JOB_TYPE_ON_SITE = 'on-site'
JOB_TYPE_HYBRID = 'hybrid'
    
    # experience level
EXPERIENCE_LEVEL_INTERNSHIP = 'internship'
EXPERIENCE_LEVEL_ENTRY_LEVEL = 'entry_level'
EXPERIENCE_LEVEL_MID_LEVEL = 'mid_level'
EXPERIENCE_LEVEL_SENIOR_LEVEL = 'senior_level'

class JobPost(models.Model):

    EXPERIENCE_LEVEL_CHOICES = [
        (EXPERIENCE_LEVEL_INTERNSHIP, 'Internship'),
        (EXPERIENCE_LEVEL_ENTRY_LEVEL, 'Entry Level'),
        (EXPERIENCE_LEVEL_MID_LEVEL, 'Mid Level'),
        (EXPERIENCE_LEVEL_SENIOR_LEVEL, 'Senior Level'),
    ]
    
    JOB_TYPE_CHOICES = [
        (JOB_TYPE_REMOTE, 'remote'),
        (JOB_TYPE_ON_SITE, 'on-site'),
        (JOB_TYPE_HYBRID, 'hybrid')
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    description = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    salary = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    date_updated = models.DateTimeField(auto_now=True)
    location = models.CharField(max_length=255, blank=True)
    job_type = models.CharField(max_length=255, choices=JOB_TYPE_CHOICES, default=JOB_TYPE_ON_SITE)
    experience_level = models.CharField(max_length=255,choices=EXPERIENCE_LEVEL_CHOICES)
    link = models.URLField()
    expire_date = models.DateTimeField(auto_now=True)
    
    

class JobApplication(models.Model):
    job = models.ForeignKey(JobPost,on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    date_applied = models.DateTimeField(auto_now=True)
    review_date = models.DateTimeField(auto_now=True)
        