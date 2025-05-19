from rest_framework import serializers
from .models import Category, Item, Delivery
from django.db.models import F

class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer for Category model.
    """
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']

class ItemSerializer(serializers.ModelSerializer):
    """
    Serializer for Item model.
    """
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    
    class Meta:
        model = Item
        fields = [
            'id', 'slug', 'name', 'description', 'category', 'quantity', 'to_json'
        ]

class DeliverySerializer(serializers.ModelSerializer):
    """
    Serializer for Delivery model.
    """
    #item = serializers.PrimaryKeyRelatedField(queryset=Item.objects.all()) 
    
    class Meta:
        model = Delivery
        fields = ['id', 'item', 'customer_name', 'phone_number', 'location', 'date', 'is_delivered']
