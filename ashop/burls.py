from django.urls import path, include
from .bviews import Home
from acs.bviews import ACSHome


urlpatterns = [
  path('',Home.as_view(),name='home'),
]