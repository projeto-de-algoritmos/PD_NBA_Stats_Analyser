from django.http import HttpResponse
from django_tables2 import SingleTableView
from django.utils.html import format_html

import django_tables2 as tables

from analyser.models import Stats

def status(request):
    return HttpResponse('Hello world')

class StatsTable(tables.Table):
    class Meta:
        model = Stats
        template_name = "django_tables2/bulma.html"
        fields = (
            "games", "player", "points", "rebounds", "assists", "blocks"
        )

class PersonListView(SingleTableView):
    model = Stats
    paginate_by = 20
    table_class = StatsTable
    template_name = 'stats.html'


