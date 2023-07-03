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
        
    thrashers = {
        'name' : 'Altlanta Thrashers',
        'id_num' : 11,
        'acronym' : 'ATL'
        }
    create_team(thrashers)
    
    yotes = {
        'name' : 'Phoenix Coyotes',
        'id_num' : 27,
        'acronym' : 'PHX'
        }
    create_team(yotes)
        
    index_list = [t.id_num for t in Team.objects.all()]
       
    #Loop through all teams to handle their rosters
    for i in index_list:
        if i not in [11, 27]:
            #Create player objects for each active player on the rosters
            roster_response = requests.get(API_URL + "/api/v1/teams/" + str(i) + "/roster", params={"Content-Type": "application/json"})
            roster_data = roster_response.json()
            
            #Get the team reference for current team
            team_key = Team.objects.filter(id_num = i)[0]
            
            print(team_key)
            
            #loop through all players of a given team's roster
            for person in roster_data["roster"]:
                person_response = requests.get(API_URL + person["person"]["link"], params={"Content-Type": "application/json"})
                person_data = person_response.json()
                
                #Create the dictionary of player data
                player_dict = {
                    'name' : person_data["people"][0]["fullName"],
                    'team' : team_key,
                    'number' : int(person_data["people"][0].get("primaryNumber",-1)),
                    'age' : person_data["people"][0].get("currentAge", -1),
                    'height' : person_data["people"][0].get("height", "N/A"),
                    'weight' : person_data["people"][0].get("weight", -1),
                    'id_num' : person_data["people"][0]["id"],
                    'country' : person_data["people"][0].get("birthCountry", "N/A"),
                    'position' : person_data["people"][0]["primaryPosition"].get("name", "N/A"),
                    'pos_code' : person_data["people"][0]["primaryPosition"].get("abbreviation", "N/A")
                    }
                player_key = create_player(player_dict)
                
                
                stat_response = requests.get(API_URL + person["person"]["link"] + "/stats?stats=yearByYear", params={"Content-Type": "application/json"})
                stat_data = stat_response.json()
                
                #Loop through each NHL season that a player has played
                for split in stat_data["stats"][0]["splits"]:
                    if split["league"]["name"] == "National Hockey League":
                        season_key = Season.objects.filter(year = int(split["season"][4:]))[0]
                        try:
                            old_team_key = Team.objects.filter(id_num = split["team"]["id"])[0]
                        except:
                            print(split["team"])
                        
                        
                        #Create stat dictionary with all information
                        stat_dict = {
                            'player' : player_key,
                            'season' : season_key,
                            'team' : old_team_key,
                            'goals' : split["stat"].get("goals", 0),
                            'assists' : split["stat"].get("assists", 0),
                            'toi' : split["stat"].get("timeOnIce", "0:0"),
                            'pim' : split["stat"].get("pim", 0),
                            'shots' : split["stat"].get("shots", 0),
                            'games' : split["stat"].get("games", 0),
                            'hits' : split["stat"].get("hits", 0),
                            'blocks' : split["stat"].get("blocked", 0),
                            'plusMinus' : split["stat"].get("plusMinus", 0),
                            'points' : split["stat"].get("points", 0),
                            'shifts' : split["stat"].get("shifts", 0),
                            'faceoffPct' : split["stat"].get("faceOffPct", 0),
                            'shotPct' : split["stat"].get("shotPct", 0),
                            'powerPlayGoals' : split["stat"].get("powerPlayGoals", 0),
                            'powerPlayPoints' : split["stat"].get("powerPlayPoints", 0),
                            'powerPlayTOI' : split["stat"].get("powerPlayTimeOnIce", 0),
                            'shortHandGoals' : split["stat"].get("shortHandedGoals", 0),
                            'shortHandPoints' : split["stat"].get("shortHandedPoints", 0),
                            'shortHandTOI' : split["stat"].get("shortHandedTimeOnIce", 0),
                            'gameWinningGoals' : split["stat"].get("gameWinningGoals", 0),
                            'overtimeGoals' : split["stat"].get("overTimeGoals", 0),
                            'evenTOI' : split["stat"].get("evenTimeOnIce", 0),
                            }
                        create_player_stats(stat_dict)
    

'''
Creates a team in the database
'''
def create_team(team_dict):
    team = Team.objects.create(**team_dict)
    return team

'''
Creates a player in the database
'''    
def create_player(player_dict):
    player = Player.objects.create(**player_dict)
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
def create_player_stats(stat_dict):
    stat = Stats.objects.create(**stat_dict)
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