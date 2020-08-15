import django_filters
from .models import Product
from django import forms

class ProductFilter(django_filters.FilterSet):
    price__gt = django_filters.NumberFilter(field_name='price', lookup_expr='gte',label='price greater than :')
    price__lt = django_filters.NumberFilter(field_name='price', lookup_expr='lte',label='price less than :')
    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains',label='Shopping for :')
    class Meta:
        model = Product
        fields = ['title','category']