# Generated by Django 4.2.13 on 2024-09-05 11:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('football', '0034_alter_fixtureevent_player'),
        ('fantasy', '0030_level_teamlevel'),
    ]

    operations = [
        migrations.CreateModel(
            name='LeagueMemberRoundPoint',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Date')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='Is deleted')),
                ('deleted_at', models.DateTimeField(blank=True, null=True, verbose_name='Deleted at')),
                ('total_point', models.DecimalField(decimal_places=2, default=0, max_digits=18, verbose_name='Points')),
                ('league', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='fantasy.fantasyleague', verbose_name='League')),
                ('league_participant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='round_points', to='fantasy.leagueparticipant', verbose_name='League participant')),
                ('round', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='football.round', verbose_name='Round')),
            ],
            options={
                'verbose_name': 'League member round point',
                'verbose_name_plural': 'League member round points',
                'db_table': 'league_member_round_point',
                'unique_together': {('league_participant', 'round')},
            },
        ),
    ]
