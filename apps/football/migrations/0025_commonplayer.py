# Generated by Django 4.2.13 on 2024-08-25 06:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('football', '0024_alter_sportmonkstype_code'),
    ]

    operations = [
        migrations.CreateModel(
            name='CommonPlayer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Date')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='Is deleted')),
                ('deleted_at', models.DateTimeField(blank=True, null=True, verbose_name='Deleted at')),
                ('fantasy_player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fantasy_player', to='football.premierleaguestatusbyplayer')),
                ('sportmonks_player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sportmonks_player', to='football.player')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
