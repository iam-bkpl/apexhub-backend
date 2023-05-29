"""apexhub URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from apexhub.settings import DEBUG, MEDIA_ROOT, MEDIA_URL

urlpatterns = [
    # path('',include('ashop.urls')),
    path('api/ashop/', include('ashop.urls')),
    path('api/acs/',include('acs.urls')),
    path('api/core/',include('core.urls')),
    path('api/admin/', admin.site.urls),
    path('api/api/', include('rest_framework.urls')),
    path('api/auth/', include('djoser.urls')),
    path('api/auth/', include('djoser.urls.jwt')),
    path('__debug__/', include('debug_toolbar.urls')),

    # mvt 
    # path('mtv/acs/', include('acs.burls')),
    path('',include('ashop.burls')),

] 
if settings.DEBUG:
    urlpatterns += static( settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
