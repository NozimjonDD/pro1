# Generated by Django 4.2.13 on 2024-08-18 14:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('football', '0004_alter_player_club_alter_player_date_of_birth'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='gender',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]