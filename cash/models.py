from django.db import models
from django.utils import timezone

class CashRegister(models.Model):
    """
    Model for tracking the cash register balance.
    """
    date = models.DateField(default=timezone.now)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Cash Register on {self.date}: {self.balance} TL"

    def reset_balance(self):
        """
        Reset the balance at the end of the day.
        """
        if self.date != timezone.now().date():
            self.balance = 0.00
            self.date = timezone.now().date()
            self.save()

class Transaction(models.Model):
    """
    Model for recording money transactions (in and out of the cash register).
    """
    CASH_IN = 'IN'
    CASH_OUT = 'OUT'

    TRANSACTION_CHOICES = [
        (CASH_IN, 'Cash In'),
        (CASH_OUT, 'Cash Out'),
    ]

    cash_register = models.ForeignKey(CashRegister, related_name="transactions", on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    transaction_type = models.CharField(choices=TRANSACTION_CHOICES, max_length=3)
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.transaction_type} - {self.amount} TL on {self.created_at}"

    def update_balance(self):
        """
        Update the cash register balance after each transaction.
        """
        if self.transaction_type == self.CASH_IN:
            self.cash_register.balance += self.amount
        else:
            self.cash_register.balance -= self.amount
        self.cash_register.save()

class Expense(models.Model):
    """
    Model for recording daily expenses (rent, bills, etc.)
    """
    name = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.name}: {self.amount} TL on {self.date}"

    class Meta:
        ordering = ['-date']
