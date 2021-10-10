from django.utils import timezone
from django.db.utils import IntegrityError

import pandas as pd

from analyser.models import Game, Player, Stats, Team


def get_teams_data(teams_df):
    """
    """
    teams_df['name'] = teams_df.apply(
        lambda row: f"{row['city']} {row['nickname']}",
        axis=1
    )
    teams_df = teams_df.rename(columns={'team_id': 'id'})
    filtered_teams_df = teams_df[['name','id', 'abbreviation']]

    teams_data = filtered_teams_df.to_dict('records')
    return teams_data

def lower_column_names(df):
    """
    """
    df.rename(columns=lambda col_name: col_name.lower(), inplace=True)
    return df

def get_games_data(games_df, games_details_df, season=2020):
    # Filter games by season
    games_df = games_df.loc[games_df['season'] == season]

    # Get only unique games IDs
    unique_games_ids = games_df.game_id.unique()
    detailed_games = games_details_df.loc[
        games_details_df['game_id'].isin(unique_games_ids)
    ]

    # Remove players that didn't played
    detailed_games = detailed_games[detailed_games['min'].notna()]

    # Merge games details and stats dataframes
    detailed_games = pd.merge(
        games_df,
        detailed_games[
            [
                'game_id','player_id','player_name', 'team_id', 'pts', 'reb', 'ast', 'blk',
                'fta', 'ftm', 'ft_pct',
                'fga', 'fgm', 'fg_pct'
            ]
        ],
        on='game_id',
        how='left'
    )

    # Filter relevant fields
    filtered_detailed_games = detailed_games[
        [
            'game_id', 'game_date_est', 'team_id', 'home_team_id', 'visitor_team_id', 'player_id', 'player_name',
            'pts', 'reb', 'ast', 'blk', 'fta', 'ftm', 'ft_pct', 'fga', 'fgm', 'fg_pct'
        ]
    ]
    
    filtered_games_data = filtered_detailed_games.to_dict('records')
    for game in filtered_games_data:
        try:
            home_team = Team.objects.get(
                id=game['home_team_id']
            )
            away_team = Team.objects.get(
                id=game['visitor_team_id']
            )
            player_team = Team.objects.get(
                id=game['team_id']
            )
        except Team.DoesNotExist:
            print('Dump the team data before running the game seed script')
            return
        else:
            try:
                game_obj, _ = Game.objects.get_or_create(
                    id=game['game_id'],
                    date=timezone.datetime.strptime(game['game_date_est'], '%Y-%m-%d'),
                    home_team=home_team,
                    away_team=away_team,
                    slug=(
                        f'{home_team.name} VS {away_team.name} - {timezone.datetime.strptime(game["game_date_est"], "%Y-%m-%d").strftime("%d/%m/%Y")}'
                    )
                )
            except IntegrityError:
                game_obj = Game.objects.get(
                    id=game['game_id'],
                    date=timezone.datetime.strptime(game['game_date_est'], '%Y-%m-%d'),
                    home_team=home_team,
                    away_team=away_team
                )
            try:
                player_obj, _ = Player.objects.get_or_create(
                    id=game["player_id"],
                    team=player_team,
                    name=game["player_name"]
                )
            except IntegrityError:
                # Player changed team, but we want to keep player associated to the latest team
                player_obj = Player.objects.get(
                    id=game["player_id"],
                    name=game["player_name"]
                )

            stats = Stats.objects.create(
                player=player_obj,
                points=game["pts"],
                rebounds=game["reb"],
                assists=game["ast"],
                blocks=game["blk"],
                free_throws_attempts=game["fta"],
                free_throws_made=game["ftm"],
                free_throws_percent=game["ft_pct"],
                field_goals_attempts=game["fga"],
                field_goals_made=game["fgm"],
                field_goals_percent=game["fg_pct"]
            )
            stats.games.add(game_obj)

    return filtered_detailed_games
