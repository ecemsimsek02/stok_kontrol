# Generated by Django 5.1 on 2025-04-09 15:00

import django_extensions.db.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='purchase',
            name='vendor',
        ),
        migrations.AlterField(
            model_name='purchase',
            name='slug',
            field=django_extensions.db.fields.AutoSlugField(blank=True, editable=False, populate_from='description', unique=True),
        ),
    ]
