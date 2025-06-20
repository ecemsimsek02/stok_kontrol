# Generated by Django 5.1 on 2025-05-14 09:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0006_alter_sale_delivery_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchase',
            name='delivery_status',
            field=models.CharField(choices=[('P', 'Pending'), ('S', 'Successful')], default='P', max_length=20, verbose_name='Delivery Status'),
        ),
    ]
