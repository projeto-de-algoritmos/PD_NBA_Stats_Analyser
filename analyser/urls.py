from analyser import views
from django.urls import path

urlpatterns = [
    path('stats/player/<int:pk>', views.player_stats, name="player_stats"),
    path('', views.home, name="home"),
    path('stats/', views.StatsListView.as_view(), name="stats"),
]