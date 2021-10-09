from django.http import HttpResponse

from django_tables2 import SingleTableView
from django_tables2.views import SingleTableMixin
from django_filters.views import FilterView

import django_tables2 as tables

from analyser.models import Stats
from analyser.filters import StatsFilter

def status(request):
    return HttpResponse('Hello world')

class StatsTable(tables.Table):
    games = tables.ManyToManyColumn(verbose_name="Game")
    player_team = tables.Column(accessor="player.team", verbose_name="Player Team")

    class Meta:
        model = Stats
        template_name = "django_tables2/bulma.html"
        fields = (
            "player", "player_team", "games", "points", "rebounds", "assists", "blocks"
        )

class StatsListView(SingleTableMixin, FilterView):
    model = Stats
    paginate_by = 20
    table_class = StatsTable
    template_name = 'stats.html'

    filterset_class = StatsFilter

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        
        stats = Stats.objects.all()[:20]

        stats_filter = StatsFilter(self.request.GET, queryset=stats)
        has_filter = any(
            field in self.request.GET for field in set(stats_filter.get_fields())
        )

        context = {
            'stats_filter':stats_filter,
            'has_filter': has_filter
        }
        table = self.get_table(**self.get_table_kwargs())
        context[self.get_context_table_name(table)] = table
        return context
