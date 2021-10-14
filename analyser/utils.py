from django.utils import timezone
from django.db.utils import IntegrityError

import pandas as pd

from analyser.models import Game, Player, Stats, Team


def update_rowspan_dict(rowspan_dict, column, row):
    """Helper to update rowspan dict avoiding KeyError"""
    if column in rowspan_dict:
        rowspan_dict[column]["length"] += 1
    else:
        rowspan_dict[column] = {
            "start": row,
            "length": 1
        }

def lower_column_names(df):
    """Lower all columns in a dataframe"""
    df.rename(columns=lambda col_name: col_name.lower(), inplace=True)
    return df

def build_player_data(player_id):
    """
    Build list of dict with player stats and 
    list with stats separately
    """
    table_data = []
    player = Player.objects.get(pk=player_id)
    subsequence_data = {
        "player_name": player.name,
        "points": [],
        "rebounds": [],
        "assists": [],
        "blocks": []
    }
    player_stats = player.stats_set.all().order_by('-id')
    for stat in player_stats:
        game = stat.games.all().first()
        table_data.append(
            {
                "player_name": player.name,
                "player_team": player.team.name,
                "game": game.slug,
                "game_date": game.date,
                "points": stat.points,
                "rebounds": stat.rebounds,
                "assists": stat.assists,
                "blocks": stat.blocks,
            }
        )

        subsequence_data["points"].append(
            (stat.points, game.slug,)
        )
        subsequence_data["rebounds"].append(
            (stat.rebounds, game.slug,)
            
        )
        subsequence_data["assists"].append(
            (stat.assists, game.slug,)
            
        )
        subsequence_data["blocks"].append(
            (stat.blocks, game.slug,)
        )

    return table_data, subsequence_data


def parse_teams_data(teams_df):
    """Parse teams data to a list of dicts using teams dataframe"""
    teams_df['name'] = teams_df.apply(
        lambda row: f"{row['city']} {row['nickname']}",
        axis=1
    )
    teams_df = teams_df.rename(columns={'team_id': 'id'})
    filtered_teams_df = teams_df[['name','id', 'abbreviation']]

    teams_data = filtered_teams_df.to_dict('records')
    return teams_data


def parse_games_data(games_df, games_details_df, season=2020):
    """
    Parse games data to a list of dicts using games and
    games details dataframe
    """
    # Filter games by season
    games_df = games_df.loc[games_df['season'] == season][:10]

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
                'game_id','player_id','player_name', 'team_id',
                'pts', 'reb', 'ast', 'blk',
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
            'game_id', 'game_date_est', 'team_id', 'home_team_id',
            'visitor_team_id', 'player_id', 'player_name',
            'pts', 'reb', 'ast', 'blk', 'fta', 'ftm',
            'ft_pct', 'fga', 'fgm', 'fg_pct'
        ]
    ]
    parsed_games_data = filtered_detailed_games.to_dict('records')

    return parsed_games_data


def save_stats_to_db(parsed_games_data):
    """
    Save stats to db after processing games,
    games details and teams dataframes
    """
    for game in parsed_games_data:
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
            game_obj = save_game_to_db(game, home_team, away_team)
            player_obj = save_player_to_db(game, player_team)

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


def save_game_to_db(game, home_team, away_team):
    """
    Save game data to db
    """
    try:
        game_obj, _ = Game.objects.get_or_create(
            id=game['game_id'],
            date=timezone.datetime.strptime(game['game_date_est'], '%Y-%m-%d'),
            home_team=home_team,
            away_team=away_team,
            slug=(
                f'{home_team.name} VS {away_team.name} - '
                f'{timezone.datetime.strptime(game["game_date_est"], "%Y-%m-%d").strftime("%d/%m/%Y")}'
            )
        )
    except IntegrityError:
        game_obj = Game.objects.get(
            id=game['game_id'],
            date=timezone.datetime.strptime(game['game_date_est'], '%Y-%m-%d'),
            home_team=home_team,
            away_team=away_team
        )
    return game_obj


def save_player_to_db(game, player_team):
    """
    Save player data to db
    """
    try:
        print("#"*30)
        print(game)
        print("#"*30)
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
    return player_obj