from django.urls import path,include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('category', views.CategoryViewSet, basename='category')
router.register('products', views.ProductViewSet, basename='product')


urlpatterns = [
    path('',include(router.urls)),
]


# urlpatterns = [
#     path('',views.CategoryView.as_view(), name='product-list'),
# ]