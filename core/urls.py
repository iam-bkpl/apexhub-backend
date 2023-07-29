from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers

from core.models import CustomUser
from . import views

router = DefaultRouter()

router.register("students", views.StudentViewSet, basename="students")
router.register("externals", views.ExternalViewSet, basename="externals")
router.register("acs", views.AcsViewSet, basename="acs")
router.register("contacts", views.ContactViewSet, basename="contacts")
router.register("users", views.CustomUserViewSet, basename="users")

student_router = routers.NestedSimpleRouter(router, "students", lookup="student")

student_router.register("ratings", views.RatingViewSet, basename="student-ratings")

urlpatterns = [path("", include(router.urls)), path("", include(student_router.urls))]
