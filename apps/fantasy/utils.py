import secrets
import string

from django.conf import settings
from django.db import transaction
from django.db.models import Q

from . import models
from apps.football import models as football_models


def generate_league_invite_code(length=6):
    chars = string.ascii_uppercase + string.digits

    code = "".join(secrets.choice(chars) for _ in range(length))
    return code


@transaction.atomic
def update_fixture_player_rnd_points(fixture):
    if fixture.state.state == "NS":
        return

    players = football_models.Player.objects.filter(
        is_deleted=False,
        club__league__remote_id=settings.PREMIER_LEAGUE_ID,
        position__isnull=False,
    ).filter(
        Q(club_id=fixture.home_club_id) |
        Q(club_id=fixture.away_club_id)
    )

    fixture_events = football_models.FixtureEvent.objects.filter(fixture_id=fixture.pk)
    fixture_stats = football_models.FixtureStatistic.objects.filter(fixture_id=fixture.pk)

    for player in players:
        try:
            player_point = models.PlayerRoundPoint.objects.get(
                player_id=player.pk,
                round_id=fixture.round_id,
            )
        except models.PlayerRoundPoint.DoesNotExist:
            player_point = models.PlayerRoundPoint(
                player_id=player.pk,
                round_id=fixture.round_id,
                total_point=0,
            )

        is_lineup = False
        try:
            lineup = football_models.Lineup.objects.get(player_id=player.pk, fixture_id=fixture.pk)
            if lineup.type.developer_name == "LINEUP":
                is_lineup = True
        except football_models.Lineup.DoesNotExist:
            player_point.total_point = 0
            player_point.minutes_played = 0
            player_point.clean_sheet = 0
            player_point.saves = 0
            player_point.penalty_save = 0
            player_point.save()
            continue

        g_upto_70 = 1
        g_more_70 = 2
        g_goal = 0
        g_goal_conceded_more_2 = 0
        g_assist = 0
        g_save_upto_3 = 0
        g_save_more_3 = 0
        g_yellow_card = 0
        g_red_card = 0
        g_penalty_miss = 0
        g_penalty_save = 0
        g_clean_sheet = 0
        g_brace = 0
        g_hat_trick = 0

        if player.position.short_name == "GK":
            g_clean_sheet = 4
            g_goal = 10
            g_assist = 6
            g_save_upto_3 = 1
            g_save_more_3 = 2
            g_yellow_card = -2
            g_red_card = -4
            g_penalty_miss = 0
            g_penalty_save = 4
            g_goal_conceded_more_2 = -1
        elif player.position.short_name == "DF":
            g_clean_sheet = 4
            g_goal = 6
            g_assist = 4
            g_save_upto_3 = 0
            g_save_more_3 = 0
            g_yellow_card = -1
            g_red_card = -3
            g_penalty_miss = 0
            g_penalty_save = 0
        elif player.position.short_name == "MF":
            g_goal = 5
            g_assist = 3
            g_yellow_card = -1
            g_red_card = -3
            g_penalty_miss = -2
            g_brace = 2
            g_hat_trick = 3
        elif player.position.short_name == "ATK":
            g_goal = 4
            g_assist = 3
            g_yellow_card = -1
            g_red_card = -3
            g_penalty_miss = -2
            g_brace = 1
            g_hat_trick = 2

        # minutes played
        subs = fixture_events.filter(
            type=football_models.SportMonksType.objects.get(developer_name="SUBSTITUTION"),
        ).filter(Q(player_id=player.pk) | Q(related_player_id=player.pk)).last()

        minutes_played = 0
        if is_lineup:
            minutes_played = 1
            if subs:
                if subs.minute <= 70:
                    minutes_played = g_upto_70
                else:
                    minutes_played = g_more_70
            else:
                if fixture.state.state == "FT":
                    minutes_played = 2
        else:
            if subs:
                if subs.minute <= 20:
                    minutes_played = g_more_70
                else:
                    minutes_played = g_upto_70

        player_point.minutes_played = minutes_played

        # goals
        goals = fixture_events.filter(player_id=player.pk, type__developer_name="GOAL").count()
        player_point.goal = goals * g_goal

        if goals == 2:
            player_point.goal += g_brace
        elif goals == 3:
            player_point.goal += g_hat_trick

        # goals conceded
        goals_conceded = None
        if is_lineup:
            if subs:
                goals_conceded = fixture_events.filter(
                    type__developer_name="GOAL",
                    minute__lte=subs.minute
                ).exclude(
                    club__id=player.club_id
                ).count()
            else:
                goals_conceded = fixture_events.filter(type__developer_name="GOAL", ).exclude(
                    club__id=player.club_id
                ).count()
        else:
            if subs:
                goals_conceded = fixture_events.filter(type__developer_name="GOAL", minute__gte=subs.minute).exclude(
                    club__id=player.club_id
                ).count()
            else:
                pass

        player_point.clean_sheet = 0
        if goals_conceded is not None:
            if fixture.state.state == "FT" and goals_conceded == 0:
                player_point.clean_sheet = g_clean_sheet
            elif goals_conceded >= 2:
                player_point.goal_conceded = g_goal_conceded_more_2

        # assists
        player_point.assist = fixture_events.filter(
            related_player_id=player.pk,
            type__developer_name="GOAL"
        ).count() * g_assist

        # saves
        if is_lineup:
            if not subs:
                saves_count = fixture_stats.filter(club__id=player.club_id).first().value
                if saves_count and saves_count <= 3:
                    player_point.saves = saves_count * g_save_upto_3
                elif saves_count and saves_count > 3:
                    player_point.saves = saves_count * g_save_more_3
        else:
            pass

        # yellow_card
        player_point.yellow_card = fixture_events.filter(
            player_id=player.pk,
            type__developer_name="YELLOWCARD"
        ).count() * g_yellow_card

        # red_card
        player_point.red_card = fixture_events.filter(
            player_id=player.pk,
        ).filter(
            Q(type__developer_name="REDCARD") | Q(type__developer_name="YELLOWREDCARD")
        ).count() * g_red_card

        player_point.total_point = player_point.calculate_total_point()
        player_point.save()

        # update squad players, team round points
        update_squad_player_points(player_point)
        update_squad_round_points(player_point)


def update_squad_player_points(player_point):
    squad_players = models.SquadPlayer.objects.filter(
        player__player_id=player_point.player_id,
        squad__round_id=player_point.round_id,
    )
    for player in squad_players:
        total_point = player_point.total_point
        if player.is_captain:
            total_point *= 2
        # TODO: check TARIFF and update total_point

        if hasattr(player, "round_point"):
            player.round_point.total_point = total_point
            player.round_point.save(update_fields=["total_point"])
        else:
            models.SquadPlayerRoundPoint.objects.create(
                squad_player_id=player.pk,
                total_point=total_point,
                round_id=player_point.round_id,
                player_point=player_point,
            )


def update_squad_round_points(player_point):
    rnd = player_point.round
    squad_player_points = models.SquadPlayerRoundPoint.objects.filter(player_point=player_point)
    squad_ids = squad_player_points.values("squad_player__squad_id").distinct()
    squads = models.Squad.objects.filter(
        round_id=rnd.pk,
        pk__in=squad_ids,
    )

    for squad in squads:
        if hasattr(squad, "round_point"):
            squad.round_point.total_point = squad.round_point.calculate_total_point()
            squad.round_point.save(update_fields=["total_point"])
        else:
            round_point = models.TeamRoundPoint.objects.create(
                team_id=squad.team_id,
                squad_id=squad.pk,
                round_id=rnd.pk,
            )
            round_point.total_point = round_point.calculate_total_point()
            round_point.save()
