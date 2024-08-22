# Generated by Django 4.2.13 on 2024-08-19 11:12

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('football', '0006_alter_player_country_id_alter_player_nationality_id'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('fantasy', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FantasyLeague',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Date')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='Is deleted')),
                ('deleted_at', models.DateTimeField(blank=True, null=True, verbose_name='Deleted at')),
                ('title', models.CharField(max_length=255, null=True, verbose_name='Title')),
                ('description', models.TextField(verbose_name='Description')),
                ('type', models.CharField(choices=[('public', 'Public'), ('private', 'Private')], max_length=100, verbose_name='Type')),
                ('invite_code', models.CharField(blank=True, max_length=50, null=True)),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fantasy_leagues', to=settings.AUTH_USER_MODEL, verbose_name='Owner')),
            ],
            options={
                'db_table': 'fantasy__league',
            },
        ),
        migrations.RemoveField(
            model_name='league',
            name='owner',
        ),
        migrations.RemoveField(
            model_name='formation',
            name='schame',
        ),
        migrations.RemoveField(
            model_name='team',
            name='title',
        ),
        migrations.AddField(
            model_name='formation',
            name='scheme',
            field=models.CharField(max_length=50, null=True, unique=True, validators=[django.core.validators.RegexValidator(message="Formation must be entered in the format: '4-4-2' or '5-2-2-1'. Up to 5 digits allowed.", regex='^\\d(-\\d){1,4}$')]),
        ),
        migrations.AddField(
            model_name='team',
            name='name',
            field=models.CharField(max_length=255, null=True, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='formation',
            name='ordering',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='leagueparticipant',
            name='team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='league_participants', to='fantasy.team', verbose_name='Team'),
        ),
        migrations.AlterField(
            model_name='team',
            name='formation',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='fantasy.formation'),
        ),
        migrations.AlterField(
            model_name='team',
            name='status',
            field=models.CharField(choices=[('active', 'Active'), ('inactive', 'Inactive')], default='inactive', max_length=100),
        ),
        migrations.AlterField(
            model_name='team',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='team', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='teamplayer',
            name='player',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='football.player'),
        ),
        migrations.AlterField(
            model_name='teamplayer',
            name='position',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='football.position'),
        ),
        migrations.AlterField(
            model_name='teamplayer',
            name='team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='team_players', to='fantasy.team'),
        ),
        migrations.AlterModelTable(
            name='formation',
            table='formation',
        ),
        migrations.AlterModelTable(
            name='leagueparticipant',
            table='fantasy_league_participant',
        ),
        migrations.AlterModelTable(
            name='team',
            table='fantasy_team',
        ),
        migrations.AlterModelTable(
            name='teamplayer',
            table='fantasy_team_player',
        ),
        migrations.DeleteModel(
            name='Position',
        ),
        migrations.AlterField(
            model_name='leagueparticipant',
            name='league',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='league_participants', to='fantasy.fantasyleague', verbose_name='League'),
        ),
        migrations.DeleteModel(
            name='League',
        ),
    ]
