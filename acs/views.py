from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from acs.models import JobApplication, JobVote
from acs.serializers import (
    JobApplicationCreateSerializer,
    JobApplicationSerializer,
    JobApplicationUpdateSerializer,
    JobVoteSerializer,
)
from django.conf import settings
from django.core.mail import send_mail
from core.models import CustomUser
from acs.permission import JobPostPermission
from .models import JobPost
from .serializers import JobPostSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
import rest_framework
import requests


class JobPostViewSet(ModelViewSet):
    serializer_class = JobPostSerializer
    # queryset = JobPost.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ["company", "title", "description", "experience_level", "location"]
    ordering_fields = ["date_added", "salary", "date_updated", "expire_date"]

    permission_classes = [JobPostPermission]

    def get_serializer_class(self):
        return super().get_serializer_class()

    def get_queryset(self):
        # user = self.request.user
        # if user.is_staff or user.is_acs or user.is_superuser or user.is_admin:
        #     return JobPost.objects.all()
        # if user.is_external:
        #     return JobPost.objects.filter(user=user)
        # return JobPost.objects.filter(is_active=True)
        return JobPost.objects.all()

    def get_serializer_context(self):
        user = self.request.user

        return {"user": user}


class JobApplicationViewSet(ModelViewSet):
    serializer_class = JobApplicationSerializer
    #  queryset = JobApplication.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ["user"]
    ordering_fields = ["date_applied", "date_review"]
    filterset_fields = ["user", "status"]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        job_id = self.kwargs["jobpost_pk"]
        if user.is_staff or user.user_type in ["acs", "external"]:
            # return JobApplication.objects.filter(job_id=job_id)
            return JobApplication.objects.filter(job_id=job_id)
        return JobApplication.objects.filter(user=user, job_id=job_id)

    def get_serializer_context(self):
        return {
            "jobpost_id": self.kwargs["jobpost_pk"],
            "user_id": self.request.user.id,
            "user_type": self.request.user.user_type,
        }

    def get_serializer_class(self):
        request_method = self.request.method
        if request_method == "POST":
            return JobApplicationCreateSerializer
        elif request_method == "GET":
            return JobApplicationSerializer
        elif request_method == "PUT" or request_method == "PATCH":
            return JobApplicationUpdateSerializer
        else:
            return JobApplicationSerializer

    def update(self, request, *args, **kwargs):
        user_type = self.request.user.user_type
        if user_type in ["acs", "external"]:
            return super().update(request, *args, **kwargs)
        else:
            return Response(
                {"detail": "You are not authorized to update this job application."},
                status=status.HTTP_403_FORBIDDEN,
            )


class JobVoteViewSet(ModelViewSet):
    serializer_class = JobVoteSerializer
    queryset = JobVote.objects.all()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["job_id"] = self.kwargs["jobpost_pk"]
        context["user_id"] = self.request.user.id
        return context

    def get_queryset(self):
        return JobVote.objects.filter(jobpost_id=self.kwargs["jobpost_pk"])
