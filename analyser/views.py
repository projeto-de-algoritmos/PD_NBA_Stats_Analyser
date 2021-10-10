from django.http import HttpResponse

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
    pagination_class = tables.paginators.LazyPaginator


    filterset_class = StatsFilter

    def get_page_data(self, table, page_number=1):
        current_page = table.paginate(
            page=self.request.GET.get("page", page_number),
            per_page=self.paginate_by
        )
        current_page_data = current_page.paginated_rows.data
        return current_page_data


    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        
        stats = Stats.objects.all()

        stats_filter = StatsFilter(self.request.GET, queryset=stats)
        has_filter = any(
            field in self.request.GET for field in set(stats_filter.get_fields())
        )

        table = self.get_table(**self.get_table_kwargs())

        current_page_data = self.get_page_data(table)
        teams = {}
        for i, data in enumerate(current_page_data):
            player_team = data.player.team.name
            game = data.games.all().first()

            if data.player.team.name in teams:
                teams[player_team]["length"] += 1
            else:
                teams[player_team] = {
                    "start": i,
                    "length": 1
                }
            if game.slug in teams:
                teams[game.slug]["length"] += 1
            else:
                teams[game.slug] = {
                    "start": i,
                    "length": 1
                }

        context = {
            'stats_filter':stats_filter,
            'has_filter': has_filter,
            'row_span_data': [
                table.columns["player_team"],
                table.columns["games"]
            ],
            'teams': teams,
            self.get_context_table_name(table): table
        }
        return context
