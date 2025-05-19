from django import forms
from .models import Transaction, Expense

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['cash_register', 'amount', 'transaction_type', 'description']

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['name', 'amount', 'date']
