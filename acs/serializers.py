from django.db.models import Count
from rest_framework import serializers
from .models import JobApplication, JobPost, JobVote
from core.serializers import CustomUserSerializer, ExternalSerializer, UserSerializer
from rest_framework.response import Response


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


class JobApplicationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobApplication
        fields = [
            "id",
            "resume",
        ]

    def create(self, validated_data):
        job_id = self.context["jobpost_id"]
        user_id = self.context["user_id"]

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
