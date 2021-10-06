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

    class Meta:
        model = Stats
        template_name = "django_tables2/bulma.html"
        fields = (
            "player", "games", "points", "rebounds", "assists", "blocks"
        )
        row_attrs = {'td': {'class': "a"}}

class PersonListView(SingleTableMixin, FilterView):
    model = Stats
    paginate_by = 20
    table_class = StatsTable
    template_name = 'stats.html'

    filterset_class = StatsFilter

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        
        stats = Stats.objects.all()[:20]

        myFilter = StatsFilter(self.request.GET, queryset=stats)

        context = {'myFilter':myFilter}
        table = self.get_table(**self.get_table_kwargs())
        context[self.get_context_table_name(table)] = table
        return context
