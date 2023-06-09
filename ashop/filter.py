from django_filters.rest_framework import FilterSet
from ashop.models import Category


class CategoryFilter(FilterSet):
  class Meta:
    model = Category
    fields = ['name']