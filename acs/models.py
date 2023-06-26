from django.db import models
from django.conf import settings
from apexhub.settings import AUTH_USER_MODEL, MEDIA_ROOT

# from core.models import Acs, External
from ashop.validators import file_size_validation
from django.core.validators import MinValueValidator, FileExtensionValidator

# job type

JOB_TYPE_REMOTE = "remote"
JOB_TYPE_ON_SITE = "on-site"
JOB_TYPE_HYBRID = "hybrid"

# experience level
EXPERIENCE_LEVEL_INTERNSHIP = "internship"
EXPERIENCE_LEVEL_ENTRY_LEVEL = "entry_level"
EXPERIENCE_LEVEL_MID_LEVEL = "mid_level"
EXPERIENCE_LEVEL_SENIOR_LEVEL = "senior_level"


class JobPost(models.Model):
    EXPERIENCE_LEVEL_CHOICES = [
        (EXPERIENCE_LEVEL_INTERNSHIP, "Internship"),
        (EXPERIENCE_LEVEL_ENTRY_LEVEL, "Entry Level"),
        (EXPERIENCE_LEVEL_MID_LEVEL, "Mid Level"),
        (EXPERIENCE_LEVEL_SENIOR_LEVEL, "Senior Level"),
    ]

    JOB_TYPE_CHOICES = [
        (JOB_TYPE_REMOTE, "remote"),
        (JOB_TYPE_ON_SITE, "on-site"),
        (JOB_TYPE_HYBRID, "hybrid"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    company = models.CharField(max_length=255, default="acs")
    # company = models.ForeignKey(External,on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    date_updated = models.DateTimeField(auto_now=True)
    location = models.CharField(max_length=255, blank=True)
    job_type = models.CharField(
        max_length=255, choices=JOB_TYPE_CHOICES, default=JOB_TYPE_ON_SITE
    )
    vacancy = models.IntegerField(default=1)
    experience_level = models.CharField(
        max_length=255,
        choices=EXPERIENCE_LEVEL_CHOICES,
        default=EXPERIENCE_LEVEL_INTERNSHIP,
    )
    link = models.URLField(blank=True, null=True)
    expire_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.title


class JobVote(models.Model):
    jobpost = models.ForeignKey(JobPost, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    # class Meta:
    #     unique_together = ('jobpost','user')


class JobApplication(models.Model):
    APPLICATION_STATUS_PENDING = "pending"
    APPLICATION_STATUS_REVIEWED = "reviewed"
    APPLICATION_STATUS_ACCEPTED = "accepted"
    APPLICATION_STATUS_REJECTED = "rejected"

    STATUS_CHOICES = [
        (APPLICATION_STATUS_PENDING, "Pending"),
        (APPLICATION_STATUS_REVIEWED, "Reviewed"),
        (APPLICATION_STATUS_ACCEPTED, "Accepted"),
        (APPLICATION_STATUS_REJECTED, "Rejected"),
    ]
    job = models.ForeignKey(JobPost, on_delete=models.CASCADE)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True
    )
    date_applied = models.DateTimeField(auto_now_add=True)
    date_review = models.DateTimeField(auto_now=True)
    resume = models.FileField(
        upload_to="resumes/",
        validators=[
            file_size_validation,
            FileExtensionValidator(allowed_extensions=["pdf", "png"]),
        ],
        blank=True,
        null=True,
    )
    is_active = models.BooleanField(default=True)
    status = models.CharField(
        max_length=255, choices=STATUS_CHOICES, default=APPLICATION_STATUS_PENDING
    )

    # class Meta:
    #     unique_together = ('user','job')

    def __str__(self):
        return f"{self.user} applied for {self.job} on {self.date_applied}"
