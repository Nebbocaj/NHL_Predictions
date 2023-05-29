import requests
import pandas as pd
import json

API_URL = "https://statsapi.web.nhl.com"

#Returns every team and their current place in the standings
def get_teams():
    
    response = requests.get(API_URL + "/api/v1/standings", params={"Content-Type": "application/json"})
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
    #/api/v1/schedule?startDate=2021-07-31&endDate=2021-10-31
    response = requests.get(API_URL + "/api/v1/schedule?startDate=2022-12-29&endDate=2022-12-29", params={"Content-Type": "application/json"})
    data = response.json()
    
    for date in data["dates"]:
        print("--- Date:", date["date"])
        for game in date["games"]:
            if game['gameType'] == 'R':
                
                #Gather all data from the API
                home_team = game["teams"]["home"]["team"]["name"]
                home_score = game['teams']['home']['score']
                away_team = game["teams"]["away"]["team"]["name"]
                away_score = game['teams']['away']['score']
                game_link = game["link"]
                game_status = get_game_status(game_link)
                print(".", away_team, "﹒", home_team, "/", away_score, ":", home_score, " ", game_status)
                    
                #Get rows for each playing team
                home_row = df.index[df['name'] == home_team][0]
                away_row = df.index[df['name'] == away_team][0]
                
                #Adjust each statistic in the row
                df.at[home_row, 'played'] += 1
                df.at[away_row, 'played'] += 1
                
                df.at[home_row, 'goalsFor'] += home_score
                df.at[away_row, 'goalsFor'] += away_score
                
                df.at[home_row, 'goalsAgainst'] += away_score
                df.at[away_row, 'goalsAgainst'] += home_score
                
                df.at[home_row, 'goalDiff'] += (home_score - away_score)
                df.at[away_row, 'goalDiff'] += (away_score - home_score)
                
                #Adjust wins iof the home team won
                if home_score > away_score:
                    df.at[home_row, 'wins'] += 1
                    df.at[home_row, 'points'] += 2
                    
                    if game_status == 'R':
                        df.at[home_row, 'rw'] += 1
                        df.at[home_row, 'row'] += 1
                        df.at[away_row, 'losses'] += 1
                    elif game_status == 'OT':
                        df.at[home_row, 'row'] += 1
                        df.at[away_row, 'otl'] += 1
                        df.at[away_row, 'points'] += 1
                    elif game_status == 'SO':
                        df.at[away_row, 'otl'] += 1
                        df.at[away_row, 'points'] += 1
                    else:
                        print("ERROR")
                    
                #Adjust wins iof the away team won
                elif away_score > home_score:
                    df.at[away_row, 'wins'] += 1
                    df.at[away_row, 'points'] += 2
                    
                    if game_status == 'R':
                        df.at[away_row, 'rw'] += 1
                        df.at[away_row, 'row'] += 1
                        df.at[home_row, 'losses'] += 1
                    elif game_status == 'OT':
                        df.at[away_row, 'row'] += 1
                        df.at[home_row, 'otl'] += 1
                        df.at[home_row, 'points'] += 1
                    elif game_status == 'SO':
                        df.at[home_row, 'otl'] += 1
                        df.at[home_row, 'points'] += 1
                    else:
                        print("ERROR")
                else:
                    print("ERROR")
                    
                #calculate point percentage
                df.at[home_row, "pointsPer"] = float(df.at[home_row, "points"]) / float(2 * df.at[home_row, "played"])
                df.at[away_row, "pointsPer"] = float(df.at[away_row, "points"]) / float(2 * df.at[away_row, "played"])

    for row in df.values.tolist():
        print(row)
#Initializes a temporary dataframe to keep track of the team data
def initialize_dataframe():
    
    labels = ['name', 'played', 'wins', 'losses', 'otl', 'points', 'pointsPer', 'rw', 'row', 'goalsFor', 'goalsAgainst', 'goalDiff']

    
    team_names = ['Anaheim Ducks', 'Arizona Coyotes', 'Boston Bruins', 'Buffalo Sabres',
                  'Calgary Flames', 'Carolina Hurricanes', 'Chicago Blackhawks', 'Colorado Avalanche', 
                  'Columbus Blue Jackets','Dallas Stars', 'Detroit Red Wings', 'Edmonton Oilers',
                  'Florida Panthers', 'Los Angeles Kings', 'Minnesota Wild', 'Montréal Canadiens', 
                  'Nashville Predators', 'New Jersey Devils', 'New York Islanders', 'New York Rangers', 
                  'Ottawa Senators', 'Philadelphia Flyers', 'Pittsburgh Penguins', 'San Jose Sharks', 
                  'Seattle Kraken', 'St. Louis Blues', 'Tampa Bay Lightning', 'Toronto Maple Leafs', 
                  'Vancouver Canucks', 'Vegas Golden Knights', 'Washington Capitals', 'Winnipeg Jets']
    
    df = pd.DataFrame(columns = labels)
    
    df['name'] = team_names
    
    for label in labels[1:]:
        df[label] = [0 for _ in team_names]
    
    return df

#Searches through the game data to determine if the game ended in regulation, OT, or SO
def get_game_status(link):
    response = requests.get(API_URL + link, params={"Content-Type": "application/json"})
    data = response.json()
    
    #Set ot and so to false initially
    status = "R"
    last_play = data["liveData"]["plays"]["allPlays"][::-1][0]

    #if the period type is ot or so, set booleans to true repectively
    if last_play['about']['periodType'] == "OVERTIME":
        status = "OT"
    elif last_play['about']['periodType'] == "SHOOTOUT":
        status = "SO"
            
    #return proper status
    return status
    
get_old_standings(2023, 5, 28)