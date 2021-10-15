from django.core.management.base import BaseCommand

import pandas as pd

from analyser.models import Team
from analyser.utils import lower_column_names, parse_teams_data


class Command(BaseCommand):
    help = 'Build graph from wikipedia page links using Kevin Bacon as starting node'

    def handle(self, *args, **options):
        teams_csv_filename = 'teams.csv'
        teams_df = pd.read_csv(teams_csv_filename)
        teams_df = lower_column_names(teams_df)

        team_data = parse_teams_data(teams_df)
        team_objects_list = [Team(**data) for data in team_data]
        Team.objects.bulk_create(team_objects_list)

        self.stdout.write(self.style.SUCCESS(f"Successfully dumped NBA teams to the database"))