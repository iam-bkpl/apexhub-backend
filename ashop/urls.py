from django.urls import path,include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from acs.views import JobVoteViewSet
from . import views






router = DefaultRouter()
router.register('categorys', views.CategoryViewSet, basename='categorys')
router.register('products', views.ProductViewSet, basename='products')
router.register('orders',views.OrderItemViewSet,basename='orders')



# router.register('esewa-request', views.EsewaViewSet,basename='esewa-request')
products_router = routers.NestedDefaultRouter(
    router, 'products', lookup='product')

products_router.register(
    'images', views.ProductImageViewSet, basename='product-images')

products_router.register('ratings', views.RatingViewSet,basename='product-ratings')
products_router.register('comments',views.CommentViewSet,basename='product-comments')

products_router.register('orderitems',views.OrderItemViewSet,basename='product-orderitems')
products_router.register('payments',views.PaymentViewSet, basename='product-payments')

urlpatterns = [
    path('',include(router.urls)),
   path('', include(products_router.urls)),

   
    # path('esewa-request/', view name='esewa-request'),
]
# ] + product_router.urls


# urlpatterns = [
#     path('',views.CategoryView.as_view(), name='product-list'),
# ]