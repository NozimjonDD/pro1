# Generated by Django 4.2.13 on 2024-09-03 13:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0008_remove_subscription_tariff_subscription_tariff'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tariff',
            old_name='annual_price',
            new_name='discount_price',
        ),
        migrations.RenameField(
            model_name='tariff',
            old_name='monthly_price',
            new_name='price',
        ),
    ]