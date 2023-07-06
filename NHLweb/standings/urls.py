from django.urls import path

from . import views

urlpatterns = [
    path("", views.team_odds, name="team_odds"),
    path("standings/", views.team_standings, name="team_standings"),
]