# Generated by Django 4.2.13 on 2024-08-30 07:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fantasy', '0026_playerroundpoint_assist_playerroundpoint_clean_sheet_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='playerroundpoint',
            name='point',
        ),
        migrations.AddField(
            model_name='playerroundpoint',
            name='total_point',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=18, verbose_name='Total points'),
        ),
    ]