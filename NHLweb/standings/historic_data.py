import requests
import pandas as pd

API_URL = "https://statsapi.web.nhl.com"

'''
Returns every team and their place in the standings as of the specified time.
'''
def get_old_standings(year, month, day):
    
    df = initialize_dataframe()
    
    if month > 8: 
        start = year
        end = year + 1
    else:
        start = year - 1
        end = year
    
    
    #Get past data from API
    response_past = requests.get(API_URL + "/api/v1/schedule?startDate=" + str(start) + "-8-1&endDate=" 
                            + str(year) + "-" + str(month) + "-" + str(day), 
                            params={"Content-Type": "application/json"})
    data_past = response_past.json()
    
    #Get the future schedule from API
    response_future = requests.get(API_URL + "/api/v1/schedule?startDate=" 
                                   + str(year) + "-" + str(month) + "-" + str(day) + "&endDate=" + 
                                   str(end) + "-7-31", params={"Content-Type": "application/json"})
    data_future = response_future.json()
    
    df = calculate_standings(data_past, df) 
    #ROEMOVE THIS LATER AS THERE IS A NEW FUNCTION BELOW
    #Get the future schedule 
    schedule = []
    for date in data_future["dates"][1:]:
        for game in date["games"]:
            if game['gameType'] == 'R':
                away_team = game["teams"]["away"]["team"]["name"]
                home_team = game["teams"]["home"]["team"]["name"]
                schedule.append([away_team, home_team])
                
    return df, schedule


'''
Gets the future schedule from specific date
'''
def get_schedule(year, month, day):
    
    if month > 8: 
        end = year + 1
    else:
        end = year
        
    #Get the future schedule from API
    response_future = requests.get(API_URL + "/api/v1/schedule?startDate=" 
                                   + str(year) + "-" + str(month) + "-" + str(day) + "&endDate=" + 
                                   str(end) + "-7-31", params={"Content-Type": "application/json"})
    data_future = response_future.json()

    #Get the future schedule 
    schedule = []
    for date in data_future["dates"][1:]:
        for game in date["games"]:
            if game['gameType'] == 'R':
                away_team = game["teams"]["away"]["team"]["name"]
                home_team = game["teams"]["home"]["team"]["name"]
                schedule.append([away_team, home_team])
                
    return schedule

'''
Initializes a temporary dataframe to keep track of the team data
'''
def initialize_dataframe():
    labels = ['name', 'conference', 'division', 'played', 'wins', 'losses', 'otl', 'points',  'rw', 'row', 'goalsFor', 'goalsAgainst', 'playoff']

    
    team_names = [['Anaheim Ducks', 'Western', 'Pacific'], 
                  ['Arizona Coyotes', 'Western', 'Central'], 
                  ['Boston Bruins', 'Eastern', 'Atlantic'], 
                  ['Buffalo Sabres', 'Eastern', 'Atlantic'],
                  ['Calgary Flames', 'Western', 'Pacific'], 
                  ['Carolina Hurricanes', 'Eastern', 'Metropolitan'], 
                  ['Chicago Blackhawks', 'Western', 'Central'], 
                  ['Colorado Avalanche', 'Western', 'Central'], 
                  ['Columbus Blue Jackets', 'Eastern', 'Metropolitan'],
                  ['Dallas Stars', 'Western', 'Central'], 
                  ['Detroit Red Wings', 'Eastern', 'Atlantic'], 
                  ['Edmonton Oilers', 'Western', 'Pacific'],
                  ['Florida Panthers', 'Eastern', 'Atlantic'],
                  ['Los Angeles Kings', 'Western', 'Pacific'], 
                  ['Minnesota Wild', 'Western', 'Central'], 
                  ['Montréal Canadiens', 'Eastern', 'Atlantic'], 
                  ['Nashville Predators', 'Western', 'Central'], 
                  ['New Jersey Devils', 'Eastern', 'Metropolitan'], 
                  ['New York Islanders', 'Eastern', 'Metropolitan'], 
                  ['New York Rangers', 'Eastern', 'Metropolitan'], 
                  ['Ottawa Senators', 'Eastern', 'Atlantic'], 
                  ['Philadelphia Flyers', 'Eastern', 'Metropolitan'], 
                  ['Pittsburgh Penguins', 'Eastern', 'Metropolitan'], 
                  ['San Jose Sharks', 'Western', 'Pacific'], 
                  ['Seattle Kraken', 'Western', 'Pacific'], 
                  ['St. Louis Blues', 'Western', 'Central'], 
                  ['Tampa Bay Lightning', 'Eastern', 'Atlantic'], 
                  ['Toronto Maple Leafs', 'Eastern', 'Atlantic'], 
                  ['Vancouver Canucks', 'Western', 'Central'], 
                  ['Vegas Golden Knights', 'Western', 'Pacific'], 
                  ['Washington Capitals', 'Eastern', 'Metropolitan'], 
                  ['Winnipeg Jets', 'Western', 'Pacific']]
    
    df = pd.DataFrame(columns = labels)
    
    #Set the name of each team
    df['name'] = [r[0] for r in team_names]
    df['conference'] = [r[1] for r in team_names]
    df['division'] = [r[2] for r in team_names]
    
    #Initialize all other stats to 0
    for label in labels[3:]:
        df[label] = [0 for _ in team_names]
    
    return df

'''        
Calcuate the standings using the data chunk from a specified time period
return the compiled dataframe
'''
def calculate_standings(data, df):
    
    #Loop through all dates from the beginning of the season until the specified date
    for date in data["dates"]:
        print(date["date"])
        for game in date["games"]:
            if game['gameType'] == 'R':
                
                #Gather all data from the API
                home_team = game["teams"]["home"]["team"]["name"]
                home_score = game['teams']['home']['score']
                away_team = game["teams"]["away"]["team"]["name"]
                away_score = game['teams']['away']['score']
                game_link = game["link"]
                game_status = get_game_status(game_link)
                    
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
                    
                #Adjust wins of the away team won
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
                
    return df

'''
Searches through the game data to determine if the game ended in regulation, OT, or SO
'''
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