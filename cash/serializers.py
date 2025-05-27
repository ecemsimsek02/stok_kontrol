from rest_framework import serializers
from .models import CashRegister, Transaction, Expense

class CashRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CashRegister
        fields = ['id', 'date', 'balance']
class TransactionSerializer(serializers.ModelSerializer):
    added_by = serializers.CharField(source='added_by.username', read_only=True)

    class Meta:
        model = Transaction
        fields = '__all__'

    def get_added_by_username(self, obj):
        return obj.added_by.username if obj.added_by else None

    def create(self, validated_data):
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            validated_data["added_by"] = request.user

        transaction = Transaction.objects.create(**validated_data)
        transaction.update_balance()
        return transaction

    def update(self, instance, validated_data):
        previous_amount = instance.amount
        previous_type = instance.transaction_type
        previous_cash_register = instance.cash_register

        new_cash_register = validated_data.get("cash_register", previous_cash_register)
        new_amount = validated_data.get("amount", previous_amount)
        new_type = validated_data.get("transaction_type", previous_type)

        if previous_type == "IN":
            previous_cash_register.balance -= previous_amount
        else:
            previous_cash_register.balance += previous_amount

        if new_type == "IN":
            new_cash_register.balance += new_amount
        else:
            new_cash_register.balance -= new_amount

        previous_cash_register.save()
        new_cash_register.save()

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance

class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = ['id', 'name', 'amount', 'date']
