# Generated by Django 4.2.13 on 2024-08-20 09:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fantasy', '0004_formationposition_squad_squadplayer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='formation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='fantasy.formation'),
        ),
    ]