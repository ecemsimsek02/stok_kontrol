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
    newCategoryName = serializers.CharField(write_only=True, required=False)
    category_name = serializers.CharField(source='category.name', read_only=True)
    
    class Meta:
        model = Item
        fields = ['id', 'slug', 'name', 'description', 'category', 'category_name',
                  'newCategoryName', 'quantity']

    def validate(self, data):
        newCategoryName = data.get('newCategoryName')
        category = data.get('category')

        if newCategoryName:
            if category:
                raise serializers.ValidationError("Hem 'category' hem 'newCategoryName' girilemez.")
        elif not category:
            raise serializers.ValidationError("'category' ya da 'newCategoryName' zorunlu.")
        return data

    def create(self, validated_data):
        newCategoryName = validated_data.pop('newCategoryName', None)
        if newCategoryName:
            category, created = Category.objects.get_or_create(name=newCategoryName)
            validated_data['category'] = category
        return super().create(validated_data)

    def update(self, instance, validated_data):
        newCategoryName = validated_data.pop('newCategoryName', None)
        if newCategoryName:
            category, created = Category.objects.get_or_create(name=newCategoryName)
            validated_data['category'] = category
        return super().update(instance, validated_data)
class DeliverySerializer(serializers.ModelSerializer):
    """
    Serializer for Delivery model.
    """
    #item = serializers.PrimaryKeyRelatedField(queryset=Item.objects.all()) 
    
    class Meta:
        model = Delivery
        fields = ['id', 'item', 'customer_name', 'phone_number', 'location', 'date', 'is_delivered']
