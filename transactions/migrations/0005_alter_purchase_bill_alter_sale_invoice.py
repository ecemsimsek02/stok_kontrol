# Generated by Django 5.1 on 2025-05-13 18:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bills', '0002_remove_bill_email'),
        ('invoice', '0002_alter_invoice_item'),
        ('transactions', '0004_alter_purchase_options_alter_sale_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchase',
            name='bill',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='bills.bill'),
        ),
        migrations.AlterField(
            model_name='sale',
            name='invoice',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='invoice.invoice'),
        ),
    ]
