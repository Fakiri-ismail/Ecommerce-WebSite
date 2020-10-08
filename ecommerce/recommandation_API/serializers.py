from rest_framework import serializers
from store.models import Product, Review

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'price', 'quantity', 'category', 'creator','created']

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'customer', 'product', 'rating', 'date_review']