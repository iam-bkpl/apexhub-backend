from django.contrib import admin
from acs.models import JobApplication, JobPost, JobVote


class JobVoteAdmin(admin.ModelAdmin):
    list_display = ["id", "jobpost"]


admin.site.register(JobPost)
admin.site.register(JobApplication)
admin.site.register(JobVote, JobVoteAdmin)
