from rest_framework.response import Response
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin, RetrieveModelMixin
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from core.models import Acs, CustomUser, External, Student, Rating
from ashop.permissions import IsAdminOrReadOnly
from .serializers import (
    AcsSerializer,
    ExternalSerializer,
    StudentSerializer,
    CustomUserSerializer,
    RatingSerializer,
)

from django.core.mail import send_mail, send_mass_mail, mail_admins, BadHeaderError


def send_mail(request):
    try:
        send_mail()
    except BadHeaderError:
        pass
    pass


class CustomUserViewSet(ModelViewSet):
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()

    def get_serializer_context(self):
        return {
            "user_id": self.request.user.id,
            "user_type": self.request.user.user_type,
        }


class StudentViewSet(ModelViewSet):
    serializer_class = StudentSerializer
    queryset = Student.objects.all()
    permission_classes = [IsAdminOrReadOnly]

    @action(detail=False, methods=["GET", "PUT"], permission_classes=[IsAuthenticated])
    def me(self, request):
        (student, created) = Student.objects.get_or_create(user_id=request.user.id)
        if request.method == "GET":
            serializers = StudentSerializer(student)
            return Response(serializers.data)
        elif request.method == "PUT":
            serializers = StudentSerializer(student, data=request.data)
            serializers.is_valid(raise_exception=True)
            serializers.save()
            return Response(serializers.data)


class ExternalViewSet(ModelViewSet):
    queryset = External.objects.all()
    serializer_class = ExternalSerializer

    @action(detail=False, methods=["GET", "PUT"])
    def me(self, request):
        (external, created) = External.objects.get_or_create(user_id=request.user.id)

        if request.method == "GET":
            serializers = ExternalSerializer(external)
            return Response(serializers.data)

        elif request.method == "PUT":
            serializers = ExternalSerializer(external, data=request.data)
            serializers.is_valid(raise_exception=True)
            serializers.save()
            return Response(serializers.data)


class AcsViewSet(ModelViewSet):
    queryset = Acs.objects.all()
    serializer_class = AcsSerializer

    @action(detail=False, methods=["GET", "PUT"])
    def me(self, request):
        (acs, created) = Acs.objects.get_or_create(user_id=request.user.id)

        if request.method == "GET":
            serializers = AcsSerializer(acs)
            return Response(serializers.data)
        elif request.method == "PUT":
            serializers = AcsSerializer(acs, data=request.data)
            serializers.is_valid(raise_exception=True)
            serializers.save()
            return Response(serializers.data)


class RatingViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        return RatingSerializer

    def get_queryset(self):
        return Rating.objects.filter(user_id=self.kwargs["student_pk"])

    def get_serializer_context(self):
        return {
            "rated_user_id": self.kwargs["student_pk"],
            "rater_id": self.request.user.id,
        }
