import rest_framework
from rest_framework.response import Response
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin, RetrieveModelMixin
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from core.models import CustomUser, Rating
from ashop.permissions import IsAdminOrReadOnly
from core.permissions import AcsPermission, ExternalPermission
from .serializers import (
    AcsSerializer,
    ExternalSerializer,
    StudentSerializer,
    CustomUserSerializer,
    RatingSerializer,
)

from djoser.views import UserViewSet
from django.core.mail import send_mail, send_mass_mail, mail_admins, BadHeaderError


def send_mail(request):
    try:
        send_mail()
    except BadHeaderError:
        pass
    pass


# class CustomUserViewSet(UserViewSet):
#     permission_classes = [IsAuthenticated]
#     # serializer_class = CustomUserSerializer
#     # queryset = CustomUser.objects.all()

#     def dispatch(self, request, *args, **kwargs):
#         self.user = request.user
#         return super().dispatch(request, *args, **kwargs)

#     def get_queryset(self):
#         user = self.request.user

#         if user.is_student:
#             # Return queryset for student user type
#             return CustomUser.objects.filter(id=user.id)

#         if user.is_external:
#             # Return queryset for external user type
#             return CustomUser.objects.filter(is_authorized_to_external=True)

#         # Return queryset for ACS user type and default queryset for other user types
#         return CustomUser.objects.all()

#     @action(detail=False, permission_classes=[IsAuthenticated])
#     def get_serializer_class(self):
#         user = self.request.user

#         if user.is_student:
#             # Return serializer class for student user type
#             return StudentSerializer

#         if user.is_acs:
#             # Return serializer class for ACS user type
#             return AcsSerializer

#         if user.is_external:
#             # Return serializer class for external user type
#             return ExternalSerializer

#         return Response("ok")

#     def get_serializer_context(self):
#         return {
#             "user_id": self.request.user.id,
#             "user_type": self.request.user.user_type,
#         }

#     @action(detail=False, methods=["GET", "PUT"], permission_classes=[IsAuthenticated])
#     def me(self, request):
#         (user, created) = CustomUser.objects.get_or_create(id=request.user.id)
#         user_type = user.user_type

#         if request.method == "GET":
#             serializers = StudentSerializer(user)
#             return Response(serializers.data)

#         elif request.method == "PUT":
#             serializers = StudentSerializer(user, data=request.data)
#             serializers.is_valid(raise_exception=True)
#             serializers.save()
#             return Response(serializers.data)


class CustomUserViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.is_student:
            return CustomUser.objects.filter(id=user.id)

        if user.is_external:
            return CustomUser.objects.filter(is_authorized_to_external=True)

        return CustomUser.objects.all()

    def get_serializer_class(self):
        user = self.request.user

        if user.is_student:
            return StudentSerializer

        if user.is_acs:
            return AcsSerializer

        if user.is_external:
            return ExternalSerializer

        return Response("ok")

    def get_serializer_context(self):
        user = self.request.user
        return {
            "user_id": user.id,
            "user_type": user.user_type,
        }

    @action(detail=False, methods=["GET", "PUT"], permission_classes=[IsAuthenticated])
    def me(self, request):
        user = self.request.user

        if request.method == "GET":
            if user.is_student:
                serializer = StudentSerializer(user)

            elif user.is_external:
                serializer = ExternalSerializer(user)

            elif user.is_acs:
                serializer = AcsSerializer(user)

            else:
                serializer = CustomUserSerializer(user)

            return Response(serializer.data)

        elif request.method == "PUT":
            serializer = StudentSerializer(user, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)


class StudentViewSet(ModelViewSet):
    serializer_class = StudentSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_serializer_context(self):
        return super().get_serializer_context()

    def get_queryset(self):
        user = self.request.user

        if user.is_student:
            # return CustomUser.objects.filter(id=user.id)
            return CustomUser.objects.all()

        elif user.is_acs:
            return CustomUser.objects.all()

        elif user.is_external:
            return CustomUser.objects.filter(is_authorized_to_external=True)

    @action(detail=False, methods=["GET", "PUT"], permission_classes=[IsAuthenticated])
    def me(self, request):
        (student, created) = CustomUser.objects.get_or_create(id=request.user.id)
        if request.method == "GET":
            serializers = StudentSerializer(student)
            return Response(serializers.data)
        elif request.method == "PUT":
            serializers = StudentSerializer(student, data=request.data)
            serializers.is_valid(raise_exception=True)
            serializers.save()
            return Response(serializers.data)


class ExternalViewSet(ModelViewSet):
    serializer_class = ExternalSerializer
    permission_classes = [ExternalPermission]

    def get_queryset(self):
        user = self.request.user

        if user.is_external:
            return CustomUser.objects.filter(id=user.id)

        return CustomUser.objects.filter(user_type=CustomUser.USER_TYPE_EXTERNAL)

    @action(detail=False, methods=["GET", "PUT"])
    def me(self, request):
        (external, created) = CustomUser.objects.get_or_create(id=request.user.id)

        if request.method == "GET":
            serializers = ExternalSerializer(external)
            return Response(serializers.data)

        elif request.method == "PUT":
            serializers = ExternalSerializer(external, data=request.data)
            serializers.is_valid(raise_exception=True)
            serializers.save()
            return Response(serializers.data)


class AcsViewSet(ModelViewSet):
    serializer_class = AcsSerializer
    permission_classes = [AcsPermission]

    def get_queryset(self):
        return CustomUser.objects.filter(user_type="acs")

    @action(detail=False, methods=["GET", "PUT"])
    def me(self, request):
        (acs, created) = CustomUser.objects.get_or_create(id=request.user.id)

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
    serializer_class = RatingSerializer

    def get_queryset(self):
        user_id = self.kwargs["student_pk"]
        return Rating.objects.filter(rated_user_id=user_id)

    def get_serializer_context(self):
        student_id = self.kwargs["student_pk"]
        return {
            "rated_user_id": student_id,
            "rater_id": self.request.user.id,
        }
