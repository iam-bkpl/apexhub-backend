from django.urls import path,include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from . import views

router = DefaultRouter()
router.register('categorys', views.CategoryViewSet, basename='categorys')
router.register('products', views.ProductViewSet, basename='products')
router.register('orders',views.OrderViewSet,basename='orders')


router.register('esewa-request', views.EsewaViewSet,basename='esewa-request')
product_router = routers.NestedDefaultRouter(router,'products', lookup='product')


product_router.register(
    'images', views.ProductImageViewSet,basename='product-images'
)
product_router.register('ratings', views.RatingViewSet,basename='product-ratings')
product_router.register('comments',views.CommentViewSet,basename='product-comments')

urlpatterns = [
    path('',include(router.urls)),
    # path('esewa-request/', view name='esewa-request'),
] + product_router.urls


# urlpatterns = [
#     path('',views.CategoryView.as_view(), name='product-list'),
# ]