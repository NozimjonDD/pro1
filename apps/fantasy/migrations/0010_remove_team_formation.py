# Generated by Django 4.2.13 on 2024-08-21 09:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fantasy', '0009_alter_fantasyleague_options_alter_formation_options_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='team',
            name='formation',
        ),
    ]
