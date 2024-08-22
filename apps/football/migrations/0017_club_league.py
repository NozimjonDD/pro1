# Generated by Django 4.2.13 on 2024-08-20 13:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('football', '0016_alter_fixture_venue_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='club',
            name='league',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='football.league', verbose_name='League'),
        ),
    ]