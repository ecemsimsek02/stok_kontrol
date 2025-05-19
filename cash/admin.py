from django.contrib import admin
from .models import CashRegister, Transaction, Expense

admin.site.register(CashRegister)
admin.site.register(Transaction)
admin.site.register(Expense)
