from django.urls import path
from . import views

urlpatterns = [
    path('',views.CategoryView.as_view(), name='product-list'),
]