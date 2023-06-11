from rest_framework import permissions
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        title="Apexhub API",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)


urlpatterns = [
    path('api/ashop/', include('ashop.urls')),
    path('api/acs/', include('acs.urls')),
    path('api/core/', include('core.urls')),
    path('admin/', admin.site.urls),
    path('api/api/', include('rest_framework.urls')),
    path('api/auth/', include('djoser.urls')),
    path('api/auth/', include('djoser.urls.jwt')),
    path('__debug__/', include('debug_toolbar.urls')),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^doc/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
# urlpatterns = [
#    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0,), name='schema-json'),
#    re_path(r'^doc/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
#    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

# ]

if settings.DEBUG:
    urlpatterns += static( settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
