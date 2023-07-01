from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_yasg import openapi
from rest_framework.views import Response

# schema_view = get_schema_view(


urlpatterns = [
    path("api/ashop/", include("ashop.urls")),
    path("api/acs/", include("acs.urls")),
    path("api/core/", include("core.urls")),
    path("admin/", admin.site.urls),
    path("api/api/", include("rest_framework.urls")),
    path("api/auth/", include("djoser.urls")),
    path("api/auth/", include("djoser.urls.jwt")),
    path("__debug__/", include("debug_toolbar.urls")),
    
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
