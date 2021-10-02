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
