from django.contrib import admin
from acs.models import JobApplication, JobPost


admin.site.register(JobPost)
admin.site.register(JobApplication)