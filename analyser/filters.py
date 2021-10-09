from django import forms
import django_filters
from django.db.models import Q

from analyser.models import Stats, Team



class StatsFilter(django_filters.FilterSet):
    TEAMS_CHOICES = [
        [team.id, team.name] for team in Team.objects.all().order_by('name')
    ]

    player__name = django_filters.CharFilter(
        widget=forms.TextInput(
            attrs={
                'class':'input',
                'placeholder': 'Player'
            }
        ),
        lookup_expr='icontains',
        label='Player'
    )
    player__team = django_filters.ChoiceFilter(
        choices=TEAMS_CHOICES,
    )
    games__home_team = django_filters.ChoiceFilter(
        choices=TEAMS_CHOICES,
        label='Teams'
    )

    games__away_team = django_filters.ChoiceFilter(
        choices=TEAMS_CHOICES,
    )


    class Meta:
        model = Stats
        fields = ("player__name", "games__home_team", "games__away_team")
