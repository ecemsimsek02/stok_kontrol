from django.contrib import admin
from .models import Sale, Purchase


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    """
    Admin interface configuration for the Sale model.
    """
    list_display = (
        'id',
        'get_customer_name',
        'get_date',
        'get_grand_total',
        'delivery_status',
    )
    search_fields = ('invoice__customer_name', 'invoice__id')
    list_filter = ('delivery_status',)
    ordering = ('-invoice__date',)
    readonly_fields = ('invoice',)

    def get_customer_name(self, obj):
        return obj.invoice.customer_name
    get_customer_name.short_description = 'Customer Name'

    def get_date(self, obj):
        return obj.invoice.date
    get_date.short_description = 'Date'

    def get_grand_total(self, obj):
        return obj.invoice.grand_total
    get_grand_total.short_description = 'Grand Total'

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    """
    Admin interface configuration for the Purchase model.
    """
    list_display = (
        'id',
        'get_institution_name',
        'get_date',
        'get_amount',
        'delivery_status',
    )
    search_fields = ('bill__institution_name', 'bill__id')
    list_filter = ('delivery_status',)
    ordering = ('-bill__date',)
    readonly_fields = ('bill',)

    def get_institution_name(self, obj):
        return obj.bill.institution_name
    get_institution_name.short_description = 'Institution'

    def get_date(self, obj):
        return obj.bill.date
    get_date.short_description = 'Date'

    def get_amount(self, obj):
        return obj.bill.amount
    get_amount.short_description = 'Amount'

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
