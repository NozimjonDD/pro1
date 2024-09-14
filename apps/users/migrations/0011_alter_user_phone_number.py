# Generated by Django 4.2.13 on 2024-09-09 13:13

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_user_coin_balance'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phone_number',
            field=models.CharField(error_messages={'unique': 'A user with that phone number already exists.'}, max_length=100, unique=True, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+99890 123 45 67'. Up to 13 digits allowed.", regex='^\\+998\\d{9}$')], verbose_name='phone number'),
        ),
    ]