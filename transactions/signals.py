from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Purchase


"""@receiver(post_save, sender=Sale)
def update_item_quantity(sender, instance, **kwargs):
    # Sale üzerinden invoice'a, oradan item'a ulaşılıyorsa:
    item = instance.invoice.item
    item.quantity -= instance.invoice.quantity  # Satış olduğu için azaltılır
    item.save()
    """