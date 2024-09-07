# Generated by Django 4.2.13 on 2024-09-07 15:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0014_remove_tariff_discount_price_remove_tariff_price_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='tarifforder',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('success', 'Success'), ('canceled', 'Canceled'), ('rejected', 'Rejected')], default='pending', max_length=100, verbose_name='Status'),
        ),
    ]