# invoice/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from invoice.models import Invoice
from transactions.models import Sale

@receiver(post_save, sender=Invoice)
def create_sale_for_invoice(sender, instance, created, **kwargs):
    if created:
        Sale.objects.create(invoice=instance)
