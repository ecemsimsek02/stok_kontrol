from django.db import models
from django_extensions.db.fields import AutoSlugField

from store.models import Item


class Invoice(models.Model):

    slug = AutoSlugField(unique=True, populate_from='date')
    date = models.DateTimeField(
        auto_now=True,
        verbose_name='Date (e.g., 2022/11/22)'
    )
    customer_name = models.CharField(max_length=30)
    contact_number = models.CharField(max_length=13)
    #item = models.ForeignKey(Item, on_delete=models.CASCADE)
    item = models.CharField(max_length=30)
    price_per_item = models.FloatField(verbose_name='Price Per Item (Ksh)')
    quantity = models.FloatField(default=0.00)
    shipping = models.FloatField(verbose_name='Shipping and Handling')
    total= models.FloatField(
        verbose_name='Total Amount (Ksh)', editable=False
    )
    grand_total = models.FloatField(
        verbose_name='Grand Total (Ksh)', editable=False
    )


    def save(self, *args, **kwargs):
        """
        Override save method to calculate total_amount and grand_total.
        total_amount = price_per_item * quantity
        grand_total = total_amount + shipping
        """
        self.total = self.price_per_item * self.quantity
        self.grand_total = self.total + self.shipping
        super(Invoice, self).save(*args, **kwargs)
    def __str__(self):
        """
        Return the invoice's slug.
        """
        return self.slug
