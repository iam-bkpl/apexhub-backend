from django.urls import path, include
from rest_framework.routers import DefaultRouter, SimpleRouter
from rest_framework_nested import routers
from . import views

# Create a default router for top-level resources
router = DefaultRouter()
router.register("categorys", views.CategoryViewSet, basename="categorys")
router.register("products", views.ProductViewSet, basename="products")

# Create a nested router for products-related resources
products_router = routers.NestedSimpleRouter(router, "products", lookup="product")
products_router.register("images", views.ProductImageViewSet, basename="product-images")
products_router.register("comments", views.CommentViewSet, basename="product-comments")
products_router.register("orders", views.OrderItemViewSet, basename="product-orders")

# Create a nested router for order-related resources
order_router = routers.NestedSimpleRouter(products_router, "orders", lookup="order")
order_router.register("payments", views.PaymentViewSet, basename="order-payments")

urlpatterns = [
    path("", include(router.urls)),
    path("", include(products_router.urls)),
    path("", include(order_router.urls)),
]
