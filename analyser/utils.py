import pandas as pd

def get_teams_data(teams_df):
    """
    """
    teams_df['name'] = teams_df.apply(
        lambda row: f"{row['city']} {row['nickname']}",
        axis=1
    )
    filtered_teams_df = teams_df[['name','team_id', 'abbreviation']]

    teams_data = filtered_teams_df.to_dict('records')
    return teams_data

def lower_column_names(df):
    """
    """
    df.rename(columns=lambda col_name: col_name.lower(), inplace=True)
    return df

def get_games_data(games_df, games_details_df, season=2020):
    games_df = games_df.loc[games_df['SEASON'] == season]
    unique_games_ids = games_df.GAME_ID.unique()
    detailed_games = games_details_df.loc[games_details_df['GAME_ID'].isin(unique_games_ids)]
    detailed_games = pd.merge(detailed_games, games_df[['GAME_ID','HOME_TEAM_ID', 'VISITOR_TEAM_ID']], on='GAME_ID', how='left')
    return detailed_games
