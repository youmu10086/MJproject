# Generated by Django 5.1.1 on 2024-10-14 06:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('apartment', '0002_alter_customer_checkouttime'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='durationType',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='roomType',
        ),
    ]
