from django.urls import path,include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers

from core.models import CustomUser
from . import views

router = DefaultRouter()
# router.register('category', views.CategoryViewSet, basename='category')
# router.register('products', views.ProductViewSet, basename='product')

# product_router = routers.NestedDefaultRouter(router,'products', lookup='product')

# product_router.register(
#     'images', views.ProductImageViewSet,basename='product-image'
# )
router.register('user',views.CustomUserViewSet)
router.register('students', views.StudentViewSet, basename='students')
router.register('externals', views.ExternalViewSet)
router.register('acs', views.AcsViewSet)


urlpatterns = [
    path('',include(router.urls)),
]
# ] + product_router.urls


# urlpatterns = [
#     path('',views.CategoryView.as_view(), name='product-list'),
# ]