from django.core.mail import send_mail, BadHeaderError, send_mass_mail, EmailMessage
from django.db.models import Count
from rest_framework import serializers
from core.models import CustomUser
from .models import JobApplication, JobPost, JobVote
from core.serializers import CustomUserSerializer, ExternalSerializer, UserSerializer
from rest_framework.response import Response
from django.conf import settings
from templated_mail.mail import BaseEmailMessage
from .send_email import send_application_email


class JobVoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobVote
        fields = ["id", "user", "jobpost"]

    def validate(self, attrs):
        user = attrs["user"]
        jobpost = attrs["jobpost"]
        print("validate function ")

        if JobVote.objects.filter(user=user, jobpost=jobpost).exists():
            JobVote.objects.filter(user=user, jobpost=jobpost).delete()
            raise serializers.ValidationError({"detail": "job vote deleted"})
        else:
            print("job voote does not exist")
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
        fields = [
            "id",
            "title",
            "company",
            "vacancy",
            "description",
            "date_added",
            "is_active",
            "salary",
            "location",
            "job_type",
            "experience_level",
            "link",
            "expire_date",
            "vote_count",
        ]

    def create(self, validated_data):
        user = self.context["user"]
        return JobPost.objects.create(user=user, **validated_data)


# def send_application_email(job, user):
#     subject = "New Job Application"
#     body = f"A new job application has been submitted.\nJob Title: {job.title}\nUser Email: {user.email}"
#     from_email = settings.EMAIL_HOST_USER

#     acs_users = CustomUser.objects.filter(user_type="acs")

#     for acs_user in acs_users:
#         to_email = acs_user.email

#     try:
#         # send_mail(subject, message, from_email, [to_email])
#         # message = BaseEmailMessage(
#         #     template_name="emails/jobapplication.html",
#         #     context={"job_title": job.title, "user_email": user.email},
#         # )
#         # message.attach_file(resume_file)
#         # message.send(to_email)
#         email = EmailMessage(subject, body, from_email, [to_email])
#         email.send()
#     except BadHeaderError:
#         pass
#     return


def send_application_update_email(job, user, status):
    subject = f"Job Application Update - {status} - "
    body = f"Hi, Your Job Application has been {status}.\nJob Title: {job.title}\n Thank You"
    from_email = settings.EMAIL_HOST_USER
    acs_users = CustomUser.objects.filter(user_type="acs")

    to_email = user.email

    try:
        email = EmailMessage(subject, body, from_email, [to_email])
        email.send()
    except BadHeaderError:
        pass
    return


class JobApplicationCreateSerializer(serializers.ModelSerializer):
    jobpost_id = serializers.ReadOnlyField()
    user_id = serializers.ReadOnlyField()

    class Meta:
        model = JobApplication
        fields = ["id", "resume", "jobpost_id", "user_id"]

    def create(self, validated_data):
        job_id = self.context["jobpost_id"]
        user_id = self.context["user_id"]
        job = JobPost.objects.get(id=job_id)
        user = CustomUser.objects.get(id=user_id)

        send_application_email.delay(job.id, user.id)

        if JobApplication.objects.filter(job_id=job_id, user_id=user_id).exists():
            raise serializers.ValidationError("Already applied for this Job ")
        else:
            return JobApplication.objects.create(
                job_id=job_id, user_id=user_id, **validated_data
            )


class JobApplicationSerializer(serializers.ModelSerializer):
    job = JobPostSerializer()
    user = UserSerializer()

    class Meta:
        model = JobApplication
        fields = ["id", "job", "user", "date_review", "resume", "is_active", "status"]


class JobApplicationUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobApplication
        fields = ["id", "date_review", "is_active", "status"]

        def update(self, instance, validated_data):
            user_type = self.context["user_type"]
            job_id = self.context["jobpost_id"]
            user_id = self.context["user_id"]
            job = JobPost.objects.get(id=job_id)

            job_application = JobApplication.objects.get(id=validated_data.get("id"))

            user = job_application.user
            status = validated_data.get["status"]
            send_application_update_email(job, user, status)

            if user_type == "acs" or user_type == "external":
                instance.date_review = validated_data.get(
                    "date_review", instance.date_review
                )
                instance.is_active = validated_data.get("is_active", instance.is_active)
                instance.status = validated_data.get("status", instance.status)
                instance.save()
                return instance
            else:
                raise serializers.ValidationError(
                    "You are not authorized to update this job application"
                )

    # def create(self ,validated_data):
    #   user_type = self.context['user_type']
    #   print("from job update serializer user type " + user_type)
    #   if user_type == 'acs' or user_type == 'external':
    #     return JobApplication.objects.create(**validated_data)
    #   else:
    #     raise serializers.ValidationError('You are not authorized to perform this option')
