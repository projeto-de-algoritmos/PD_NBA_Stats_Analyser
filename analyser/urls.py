from analyser import views
from django.urls import path

urlpatterns = [
    path('status/', views.status),
    path('home/', views.StatsListView.as_view(), name="home"),
]
# Possible error migrating db https://stackoverflow.com/questions/40549437/django-migration-relation-does-not-exist