from django.urls import path

from . import views

urlpatterns = [
    path("", views.player_page, name="player_page"),
    path("goalie/", views.goalie_page, name="goalie_page"),
]