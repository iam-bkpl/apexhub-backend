from django.contrib import admin
from acs.models import JobApplication, JobPost, JobVote


class JobVoteAdmin(admin.ModelAdmin):
    list_display = ["id", "jobpost"]


class JobAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "user"]


admin.site.register(JobPost, JobAdmin)
admin.site.register(JobApplication)
admin.site.register(JobVote, JobVoteAdmin)
