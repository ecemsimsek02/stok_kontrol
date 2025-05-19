from rest_framework import serializers
from .models import Sale, Purchase

class SaleTransactionSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source='invoice.customer_name', read_only=True)
    contact_number = serializers.CharField(source='invoice.contact_number', read_only=True)
    item = serializers.CharField(source='invoice.item', read_only=True)
    price_per_item = serializers.FloatField(source='invoice.price_per_item', read_only=True)
    quantity = serializers.FloatField(source='invoice.quantity', read_only=True)
    shipping = serializers.FloatField(source='invoice.shipping', read_only=True)
    total = serializers.FloatField(source='invoice.total', read_only=True)
    grand_total = serializers.FloatField(source='invoice.grand_total', read_only=True)
    date = serializers.DateTimeField(source='invoice.date', read_only=True)

    class Meta:
        model = Sale
        fields = [
            'id', 'invoice', 'date', 'customer_name', 'contact_number', 'item',
            'price_per_item', 'quantity', 'shipping', 'total', 'grand_total',
            'delivery_status'
        ]
class PurchaseTransactionSerializer(serializers.ModelSerializer):
    institution_name = serializers.CharField(source='bill.institution_name', read_only=True)
    phone_number = serializers.IntegerField(source='bill.phone_number', read_only=True)
    address = serializers.CharField(source='bill.address', read_only=True)
    description = serializers.CharField(source='bill.description', read_only=True)
    payment_details = serializers.CharField(source='bill.payment_details', read_only=True)
    amount = serializers.FloatField(source='bill.amount', read_only=True)
    status = serializers.BooleanField(source='bill.status', read_only=True)
    date = serializers.DateTimeField(source='bill.date', read_only=True)

    class Meta:
        model = Purchase
        fields = [
            'id', 'bill', 'date', 'institution_name', 'phone_number', 'address',
            'description', 'payment_details', 'amount', 'status',
            'delivery_status'
        ]
