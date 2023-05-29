import requests
import pandas as pd
import json

API_URL = "https://statsapi.web.nhl.com/api/v1"

#Returns every team and their current place in the standings
def get_teams():
    
    response = requests.get(API_URL + "/standings", params={"Content-Type": "application/json"})
    data = response.json()
    
    team_list = []
    
    for div in range(4):
        for i in range(8):
            
            team_list.append([data["records"][div]["teamRecords"][i]["team"]["name"],
                              data["records"][div]["teamRecords"][i]["leagueRecord"]["wins"],
                              data["records"][div]["teamRecords"][i]["leagueRecord"]["losses"],
                              data["records"][div]["teamRecords"][i]["leagueRecord"]["ot"],
                              data["records"][div]["teamRecords"][i]["points"],
                              data["records"][div]["teamRecords"][i]["pointsPercentage"],
                              data["records"][div]["teamRecords"][i]["regulationWins"],
                              data["records"][div]["teamRecords"][i]["row"],
                              data["records"][div]["teamRecords"][i]["goalsScored"],
                              data["records"][div]["teamRecords"][i]["goalsAgainst"],
                              data["records"][div]["teamRecords"][i]["goalsScored"] - data["records"][div]["teamRecords"][i]["goalsAgainst"]])

    return team_list

#Returns every team and their place in the standings as of the specified time.
def get_old_standings(year, month, day):
    
    df = initialize_dataframe()
    
    response = requests.get(API_URL + "/schedule?startDate=2021-07-31&endDate=2021-10-31", params={"Content-Type": "application/json"})
    data = response.json()
    
    for date in data["dates"]:
        
        for game in date["games"]:
            if game['gameType'] == 'R':
                pass
                #print(".", game["teams"]["away"]["team"]["name"], "﹒", game["teams"]["home"]["team"]["name"], 
                 # "/", f"{game['teams']['away']['score']}:{game['teams']['home']['score']}", "/", 
                  #game["status"]["detailedState"])
                  
#Initializes a temporary dataframe to keep track of the team data
def initialize_dataframe():
    
    labels = ['name', 'played', 'wins', 'losses', 'otl', 'points', 'pointsPer', 'rw', 'row', 'goalsFor', 'goalsAgainst', 'goalDiff']

    
    team_names = ['Anaheim Ducks', 'Arizona Coyotes', 'Boston Bruins', 'Buffalo Sabres',
                  'Calgary Flames', 'Carolina Hurricanes', 'Chicago Blackhawks', 'Colorado Avalanche', 
                  'Columbus Blue Jackets','Dallas Stars', 'Detroit Red Wings', 'Edmonton Oilers',
                  'Florida Panthers', 'Los Angeles Kings', 'Minnesota Wild', 'Montréal Canadiens', 
                  'Nashville Predators', 'New Jersey Devils', 'New York Islanders', 'New York Rangers', 
                  'Ottawa Senators', 'Philidelphia Flyers', 'Pittsburgh Penguins', 'San Jose Sharks', 
                  'Seattle Kraken', 'St. Louis Blues', 'Tampa Bay Lightning', 'Toronto Maple Leafs', 
                  'Vancouver Canucks', 'Vegas Golden Knights', 'Washington Capitals', 'Winnipeg Jets']
    
    df = pd.DataFrame(columns = labels)
    
    df['name'] = team_names
    
    for label in labels[1:]:
        df[label] = [0 for _ in team_names]
    
    return df
    
    
get_old_standings(2023, 5, 28)