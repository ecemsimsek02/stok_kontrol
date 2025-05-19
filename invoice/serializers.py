from rest_framework import serializers
from .models import Invoice

class InvoiceSerializer(serializers.ModelSerializer):
    """
    Serializer for the Invoice model.
    """
    class Meta:
        model = Invoice
        fields = [
            'id', 'customer_name', 'contact_number', 'item',
            'price_per_item', 'quantity', 'shipping', 'total','grand_total'
        ]
        read_only_fields = ('total', 'grand_total') 

    """def create(self, validated_data):
       
        validated_data['total_amount'] = validated_data['price_per_item'] * validated_data['quantity']
        return super().create(validated_data)

    def update(self, instance, validated_data):
        
        validated_data['total_amount'] = validated_data['price_per_item'] * validated_data['quantity']
        return super().update(instance, validated_data)
"""