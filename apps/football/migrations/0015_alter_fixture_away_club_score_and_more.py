# Generated by Django 4.2.13 on 2024-08-19 14:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('football', '0014_alter_clubplayer_kit_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fixture',
            name='away_club_score',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='fixture',
            name='home_club_score',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
