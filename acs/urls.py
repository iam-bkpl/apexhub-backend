from django.urls import path,include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers

from . import views

router = DefaultRouter()
router.register('jobpost', views.JobPostViewSet, basename='jobpost')
router.register('jobapplication', views.JobApplicationViewSet, basename='jobapplication')


urlpatterns = [
path('',include(router.urls)),
]