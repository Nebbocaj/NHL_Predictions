from django.urls import path

from . import views

urlpatterns = [
    path("", views.player_page, name="player_page"),
    path("<int:id_num>/", views.player_details, name='player_details'),
    path("goalie/", views.goalie_page, name="goalie_page"),
    path("goalie/<int:id_num>/", views.goalie_details, name="goalie_details"),
    path("testing/", views.testing, name="testing"),
]