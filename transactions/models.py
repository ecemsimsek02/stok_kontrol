from django.db import models
from django_extensions.db.fields import AutoSlugField

from store.models import Item
from accounts.models import Vendor, Customer
from bills.models import Bill
from invoice.models import Invoice

DELIVERY_CHOICES = [("P", "Pending"), ("S", "Successful")]

class Sale(models.Model):
    """
    Represents a sale transaction involving an invoice.
    Stores only delivery_status; other details are referenced from Invoice.
    """
    invoice = models.OneToOneField("invoice.Invoice", on_delete=models.CASCADE,null=True)
    delivery_status = models.CharField(
        choices=DELIVERY_CHOICES,
        max_length=20,
        default="P",
        verbose_name="Delivery Status"
    )

    def __str__(self):
        return f"Sale for Invoice {self.invoice.slug}"


class Purchase(models.Model):
    """
    Represents a purchase transaction involving a bill.
    Stores only delivery_status; other details are referenced from Bill.
    """
    bill = models.OneToOneField("bills.Bill", on_delete=models.CASCADE,null=True)
    delivery_status = models.CharField(
        choices=DELIVERY_CHOICES,
        max_length=20,
        default="P",
        verbose_name="Delivery Status"
    )

    def __str__(self):
        return f"Purchase for Bill {self.bill.slug}"

