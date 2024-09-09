# Generated by Django 4.2.13 on 2024-08-31 06:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('football', '0032_alter_club_remote_id_alter_clubplayer_remote_id_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='club',
            name='kit',
        ),
        migrations.AddField(
            model_name='club',
            name='kit_away',
            field=models.ImageField(blank=True, null=True, upload_to='football/club/kit_away/'),
        ),
        migrations.AddField(
            model_name='club',
            name='kit_home',
            field=models.ImageField(blank=True, null=True, upload_to='football/club/kit_home/'),
        ),
    ]
