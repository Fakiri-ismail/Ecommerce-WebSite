from import_export import resources
from .models import Product, Review

class ProductResource(resources.ModelResource):
    class Meta:
        model = Product

class ReviewResource(resources.ModelResource):
    class Meta:
        model = Review