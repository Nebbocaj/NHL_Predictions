import requests
import pandas as pd
import numpy as np
from datetime import date

from .models import Player, Season, Stats

API_URL = "https://statsapi.web.nhl.com"


def update_players():
    
    all_players = Player.objects.all()
    all_players.delete()
    all_seasons = Season.objects.all()
    all_seasons.delete()
    all_stats = Stats.objects.all()
    all_stats.delete()
    
    play_names = ["bob", "billy", "dipshit"]
    
    for player_name in play_names:
        player = create_player(player_name)
    
    season_year = [2021, 2022, 2023]
    for seas in season_year:
        season = create_season(seas)
        
    ps = Player.objects.all()
    ss = Season.objects.all()
    
    
    for p in ps:
        if p.name == "dipshit":
            s = Season.objects.get(year = 2022)
            stat = create_player_stats(p, s, 0, 0)
        else:
            for s in ss:
                stat = create_player_stats(p, s, 0, 0)
                print(f"Player: {stat.player.name}")
                print(f"Season: {stat.season.year}")
                print(f"Goals: {stat.goals}")
                print(f"Assists: {stat.assists}")

def create_player(player_name):
    player = Player.objects.create(name=player_name)
    return player

def create_season(season_year):
    season = Season.objects.create(year=season_year)
    return season

def create_player_stats(player, season, goals, assists):
    stat = Stats.objects.create(player=player, season=season, goals=goals, assists=assists)
    return stat


