from rest_framework import serializers
from .models import CashRegister, Transaction, Expense

class CashRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CashRegister
        fields = ['id', 'date', 'balance']
class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'

    def create(self, validated_data):
        transaction = Transaction.objects.create(**validated_data)
        cash_register = transaction.cash_register

        # Eğer işlem türü 'IN' ise bakiyeyi artır, 'OUT' ise azalt
        if transaction.transaction_type == 'IN':
            cash_register.balance += transaction.amount
        elif transaction.transaction_type == 'OUT':
            cash_register.balance -= transaction.amount
        
        # Son güncellenmiş bakiyeyi kaydet
        cash_register.save()
        return transaction

    def update(self, instance, validated_data):
        # Eski işlem bilgilerini al
        previous_amount = instance.amount
        previous_type = instance.transaction_type
        previous_cash_register = instance.cash_register

        # Yeni değerleri al
        new_cash_register = validated_data.get("cash_register", previous_cash_register)
        new_amount = validated_data.get("amount", previous_amount)
        new_type = validated_data.get("transaction_type", previous_type)

        # Eski işlem değerini geri al
        if previous_type == "IN":
            previous_cash_register.balance -= previous_amount
        else:
            previous_cash_register.balance += previous_amount

        # Yeni değerle işlemi güncelle
        if new_type == "IN":
            new_cash_register.balance += new_amount
        else:
            new_cash_register.balance -= new_amount

        # Son bakiyeyi kaydet
        previous_cash_register.save()
        new_cash_register.save()

        # Modeli güncelle
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance


class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = ['id', 'name', 'amount', 'date']
