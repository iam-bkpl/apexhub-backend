from django.urls import path,include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers

from . import views

router = DefaultRouter()
router.register('jobpost', views.JobPostViewSet, basename='jobpost')
# router.register('jobapplication', views.JobApplicationViewSet, basename='jobapplication')

jobpost_router = routers.NestedDefaultRouter(router, 'jobpost',lookup='jobpost')


jobpost_router.register(
  'applications', views.JobApplicationViewSet, basename='jobpost-applications'
)
jobpost_router.register('votes',views.JobVoteViewSet, basename='job-votes')


urlpatterns = [
path('',include(router.urls)),
]+ jobpost_router.urls

