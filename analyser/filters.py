from django import forms
import django_filters

from analyser.models import Stats



class StatsFilter(django_filters.FilterSet):
    player__name = django_filters.CharFilter(
        widget=forms.TextInput(
            attrs={
                'class':'input'
            }
        ),
        lookup_expr='icontains',
    )

    class Meta:
        model = Stats
        fields = ("player__name",)