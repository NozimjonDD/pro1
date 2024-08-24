# Generated by Django 4.2.13 on 2024-08-24 12:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('football', '0024_alter_sportmonkstype_code'),
        ('fantasy', '0023_alter_leagueparticipant_unique_together'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fantasyleague',
            name='end_time',
        ),
        migrations.RemoveField(
            model_name='fantasyleague',
            name='start_time',
        ),
        migrations.AddField(
            model_name='fantasyleague',
            name='ending_round',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='football.round', verbose_name='Ending round'),
        ),
        migrations.AddField(
            model_name='fantasyleague',
            name='starting_round',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='football.round', verbose_name='Starting round'),
        ),
    ]
