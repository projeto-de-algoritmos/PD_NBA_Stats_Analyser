from analyser import views
from django.urls import path

urlpatterns = [
    path('status/<int:pk>', views.status, name="status"),
    path('home/', views.StatsListView.as_view(), name="home"),
]
# Possible error migrating db https://stackoverflow.com/questions/40549437/django-migration-relation-does-not-exist