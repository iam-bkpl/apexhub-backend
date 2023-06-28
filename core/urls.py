from django.urls import path, include
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
router.register("users", views.CustomUserViewSet, basename="users")
router.register("students", views.StudentViewSet, basename="students")
router.register("externals", views.ExternalViewSet, basename="externals")
router.register("acs", views.AcsViewSet, basename="acs")

student_router = routers.NestedSimpleRouter(router, "students", lookup="student")

student_router.register("ratings", views.RatingViewSet, basename="student-ratings")

urlpatterns = [
    path("", include(router.urls)),
    # ]
] + student_router.urls


# urlpatterns = [
#     path('',views.CategoryView.as_view(), name='product-list'),
# ]
