from rest_framework import serializers
from .models import Bill

class BillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bill
        fields = [
            'id',
            'institution_name',
            'phone_number',
            'address',
            'description',
            'payment_details',
            'amount',
            'status'
        ]
