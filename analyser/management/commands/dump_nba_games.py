from django.core.management.base import BaseCommand

import pandas as pd

from analyser.utils import lower_column_names, get_games_data


class Command(BaseCommand):
    help = 'Build graph from wikipedia page links using Kevin Bacon as starting node'

    def handle(self, *args, **options):
        games_csv_filename = 'games.csv'
        games_df = pd.read_csv(games_csv_filename)
        games_df = lower_column_names(games_df)

        games_details_csv_filename = 'games_details.csv'
        games_details_df = pd.read_csv(games_details_csv_filename)
        games_details_df = lower_column_names(games_details_df)

        get_games_data(games_df, games_details_df)

        self.stdout.write(self.style.SUCCESS(f"Successfully dumped NBA games to the database"))