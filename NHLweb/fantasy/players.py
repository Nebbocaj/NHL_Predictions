import requests
import pandas as pd
import numpy as np
from datetime import date

from .models import Player, Season, Stats, Team

API_URL = "https://statsapi.web.nhl.com"
CURRENT_SEASON = 2024

'''
perform a full reset on the players database. 
Search through the rosters of every team and creates data for players and teams.
Also creates stats entries for each year a given player is in the league.
'''
def reset_data():
    
    #Delete all current entries
    all_teams = Team.objects.all()
    all_teams.delete()
    all_players = Player.objects.all()
    all_players.delete()
    all_seasons = Season.objects.all()
    all_seasons.delete()
    all_stats = Stats.objects.all()
    all_stats.delete()
    
    
    #Create all season objects from 1980 onward
    for y in range(1980,CURRENT_SEASON):
        create_season(y, False)
    
    #Creates an object for the current season
    create_season(CURRENT_SEASON, True)
    
    
    #Create all team objects for the 32 current teams
    team_response = requests.get(API_URL + "/api/v1/teams", params={"Content-Type": "application/json"})
    team_data = team_response.json()
    for t in team_data["teams"]:
        
        team_dict = {
            'name' : t["name"],
            'division' : t["division"]["name"],
            'conference' : t["conference"]["name"],
            'acronym' : t["abbreviation"],
            'id_num' : int(t["id"])
            }
        
        create_team(team_dict)
        
        
    #Create player objects for each active player on the rosters
    
    #Create stats objects for each season that a player has played
    

'''
Creates a team in the database
'''
def create_team(team_dict):
    team = Team.objects.create(**team_dict)
    return team

'''
Creates a player in the database
'''    
def create_player(player_name, team):
    player = Player.objects.create(name=player_name, team=team)
    return player

'''
Creates a season in the database
'''
def create_season(season_year, current):
    season = Season.objects.create(year=season_year, current_season=current)
    return season

'''
Creates a stat entry in the database
'''
def create_player_stats(player, season, goals, assists):
    stat = Stats.objects.create(player=player, season=season, goals=goals, assists=assists)
    return stat


    # all_players = Player.objects.all()
    # all_players.delete()
    # all_seasons = Season.objects.all()
    # all_seasons.delete()
    # all_stats = Stats.objects.all()
    # all_stats.delete()
    
    # team = Team.objects.create(name="BULLDOGS", division="X", conference="Y", acronym = "BDG", id_num=-1)
    
    # play_names = ["bob", "billy", "dipshit"]
    
    # for player_name in play_names:
    #     player = create_player(player_name, team)
    
    # season_year = [2021, 2022, 2023]
    # for seas in season_year:
    #     season = create_season(seas)
        


        
    # ps = Player.objects.all()
    # ss = Season.objects.all()
    
    
    # for p in ps:
    #     if p.name == "dipshit":
    #         s = Season.objects.get(year = 2022)
    #         stat = create_player_stats(p, s, 0, 0)
    #     else:
    #         for s in ss:
    #             stat = create_player_stats(p, s, 0, 0)
    #             print(f"Player: {stat.player.name}")
    #             print(f"Team: {stat.player.team.acronym}")
    #             print(f"Season: {stat.season.year}")
    #             print(f"Goals: {stat.goals}")
    #             print(f"Assists: {stat.assists}")