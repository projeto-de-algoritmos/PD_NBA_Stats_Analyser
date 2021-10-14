from django.shortcuts import render

from django_tables2.views import SingleTableMixin
from django_filters.views import FilterView
from django_tables2.utils import A

import django_tables2 as tables
from django_tables2.config import RequestConfig


from analyser.models import Stats
from analyser.utils import build_player_data
from analyser.filters import StatsFilter
from analyser.algorithms import longest_subsequence


class PlayerTable(tables.Table):
    player_name = tables.Column()
    player_team = tables.Column()
    game = tables.Column(order_by=("game_date"))
    game_date = tables.Column(visible=False)
    points = tables.Column()
    rebounds = tables.Column()
    assists = tables.Column()
    blocks = tables.Column()



def player_stats(request, pk):
    player_table_data, subsequence_data = build_player_data(pk)
    table = PlayerTable(data=player_table_data)

    RequestConfig(request, paginate={"per_page":10}).configure(table)
    
    analysis_criteria = {
        "points": {
            "selected": False
        },
        "rebounds": {
            "selected": False
        },
        "assists": {
            "selected": False
        },
        "blocks": {
            "selected": False
        },
    }

    criteria = request.GET.get("criteria", "points")
    analysis_criteria[criteria]["selected"] = True


    context = {
        "table": table,
        "analysis_criteria": analysis_criteria,
        "criteria": criteria,
        "subsequence": longest_subsequence(subsequence_data[criteria]),
        "player_name": subsequence_data["player_name"],
        "player_id": pk,
    }

    return render(request, 'player.html', context)


def home(request):
    return render(request, 'home.html')

class StatsTable(tables.Table):
    games = tables.ManyToManyColumn(verbose_name="Game")
    player = tables.LinkColumn("player_stats", args=[A("player.id")])
    id = tables.Column(verbose_name="Player team")

    def render_id(self, value, record):
        player = record.player
        game = record.games.all().first()
        home_team = player.teams.filter(id=game.home_team.id).first()
        player_team = home_team.name if home_team else player.teams.filter(id=game.away_team.id).first().name
        return player_team

    class Meta:
        model = Stats
        fields = (
            "player", "id", "games", "points", "rebounds", "assists", "blocks"
        )

class StatsListView(SingleTableMixin, FilterView):
    model = Stats
    paginate_by = 20
    table_class = StatsTable
    template_name = 'stats.html'
    pagination_class = tables.paginators.LazyPaginator
    filterset_class = StatsFilter
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        
        stats = Stats.objects.all()
        stats_filter = StatsFilter(self.request.GET, queryset=stats)

        has_filter = any(
            field in self.request.GET for field in set(stats_filter.get_fields())
        )

        table = self.get_table(**self.get_table_kwargs(), orderable=False)

        context = {
            'stats_filter':stats_filter,
            'has_filter': has_filter,
            self.get_context_table_name(table): table
        }
        return context
