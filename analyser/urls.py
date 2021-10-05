from analyser import views
from django.urls import path

urlpatterns = [
    path('status/', views.status),
    path('home/', views.PersonListView.as_view()),
]