# Generated by Django 4.2.13 on 2024-08-20 11:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_alter_user_role'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='balance',
            field=models.DecimalField(decimal_places=2, default=1000000000, max_digits=18, verbose_name='Balance'),
        ),
    ]
