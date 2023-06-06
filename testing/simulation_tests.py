import requests
import pandas as pd
import numpy as np
import random
from datetime import date
	
import time


API_URL = "https://statsapi.web.nhl.com"

                  
'''
Simulates the remaining part of the NHL season from a given point.
Takes the current standings and future schedule as input and returns a 
single possible outcome based off of a teams win probabilities
'''
def simulate_season(new_df, schedule):
    
    df = new_df.copy(deep=True)
    
    #Odd of a game going to overtime
    ot_odds = 0.25
    
    #Odds of a game going to shootout
    so_odds = 0.08
    
    #Odds that the home team will win
    #WILL CHANGE ONCE AN ELO SYSTEM IS IMPLEMENTED
    home_win = 0.5
    
    #loop through every future game of the season and
    #simulate results via the random variables
    for game in schedule:
        away_team = game[0]
        home_team = game[1]
        
        #Get rows for each playing team
        home_row = df.index[df['name'] == home_team][0]
        away_row = df.index[df['name'] == away_team][0]
        
        #determine if a game goes to overtime or a shootout froma random value
        type_event = random.uniform(0,1)
        
        #determine the winner from a random value
        win_event = random.uniform(0,1)
        
        #Increase the team's games played
        df.at[home_row, 'played'] += 1
        df.at[away_row, 'played'] += 1
        
        #If the event is a shootout...
        if type_event <= so_odds:
            if win_event < home_win:
                df.at[home_row, 'wins'] += 1
                df.at[home_row, 'points'] += 2
                df.at[away_row, 'otl'] += 1
                df.at[away_row, 'points'] += 1
            else:
                df.at[away_row, 'wins'] += 1
                df.at[away_row, 'points'] += 2
                df.at[home_row, 'otl'] += 1
                df.at[home_row, 'points'] += 1
                
        #if the event is overtime...
        elif type_event <= ot_odds:
            if win_event < home_win:
                df.at[home_row, 'wins'] += 1
                df.at[home_row, 'points'] += 2
                df.at[home_row, 'row'] += 1
                df.at[away_row, 'otl'] += 1
                df.at[away_row, 'points'] += 1
            else:
                df.at[away_row, 'wins'] += 1
                df.at[away_row, 'points'] += 2
                df.at[away_row, 'row'] += 1
                df.at[home_row, 'otl'] += 1
                df.at[home_row, 'points'] += 1
           
        #if the event is regulation...
        else:
            if win_event < home_win:
                df.at[home_row, 'wins'] += 1
                df.at[home_row, 'points'] += 2
                df.at[home_row, 'rw'] += 1
                df.at[home_row, 'row'] += 1
                df.at[away_row, 'losses'] += 1
            else:
                df.at[away_row, 'wins'] += 1
                df.at[away_row, 'points'] += 2
                df.at[away_row, 'rw'] += 1
                df.at[away_row, 'row'] += 1
                df.at[home_row, 'losses'] += 1
    return df


def simulate_season2(new_df, schedule):
    
    df = new_df.copy(deep=True)
    
    #Odd of a game going to overtime
    ot_odds = 0.25
    
    #Odds of a game going to shootout
    so_odds = 0.08
    
    #Odds that the home team will win
    #WILL CHANGE ONCE AN ELO SYSTEM IS IMPLEMENTED
    home_win = 0.5
    
    num_games = len(schedule)
    type_events = np.random.uniform(0, 1, num_games)
    win_events = np.random.uniform(0, 1, num_games)
    
    home_teams = np.array([game[1] for game in schedule])
    away_teams = np.array([game[0] for game in schedule])
    
    so_mask = type_events <= so_odds
    ot_mask = (type_events <= ot_odds) & (type_events > so_odds)
    reg_mask = type_events > ot_odds
    home_mask = win_events <= home_win
    away_mask = win_events > home_win

    
    home_so_mask = home_mask & so_mask
    home_ot_mask = home_mask & ot_mask
    home_reg_mask = home_mask & reg_mask
    away_so_mask = away_mask & so_mask
    away_ot_mask = away_mask & ot_mask
    away_reg_mask = away_mask & reg_mask
    
    
    home_win_mask = home_so_mask | home_ot_mask | home_reg_mask
    away_win_mask = away_so_mask | away_ot_mask | away_reg_mask
    home_otl_mask = home_so_mask | home_ot_mask
    away_otl_mask = away_so_mask | away_ot_mask
    home_row_mask = home_reg_mask | home_ot_mask
    away_row_mask = away_reg_mask | away_ot_mask
    
    #print(len(home_teams[home_win_mask]), len(away_teams[away_win_mask]), num_games)
    win_counts = pd.Series(home_teams[home_win_mask]).value_counts() + \
        pd.Series(away_teams[away_win_mask]).value_counts()
    df['wins'] += df['name'].map(win_counts).fillna(0)
    
    loss_counts = pd.Series(home_teams[away_reg_mask]).value_counts() + \
        pd.Series(away_teams[home_reg_mask]).value_counts()
    df['losses'] += df['name'].map(loss_counts).fillna(0)
    
    otl_counts = pd.Series(home_teams[away_otl_mask]).value_counts() + \
        pd.Series(away_teams[home_otl_mask]).value_counts()
    df['otl'] += df['name'].map(otl_counts).fillna(0)
    
    rw_counts = pd.Series(home_teams[home_reg_mask]).value_counts() + \
        pd.Series(away_teams[away_reg_mask]).value_counts()
    df['rw'] += df['name'].map(rw_counts).fillna(0)
    
    row_counts = pd.Series(home_teams[home_row_mask]).value_counts() + \
        pd.Series(away_teams[away_row_mask]).value_counts()
    df['row'] += df['name'].map(row_counts).fillna(0)
    
    df['points'] = 2 * df['wins'] + df['otl']
    
    df['played'] += df['wins'] + df['losses'] + df['otl']
    
    return df



'''
takes standings and runs simulations.
returns playoff odds for each team
'''
def get_playoff_odds(df, schedule, runs = 1000):
    
    df = df.copy(deep=True)
    
    start = time.time()
    for i in range(runs):
        
        
        print(i)
        simmed = simulate_season2(df, schedule)
    
        playoff_teams = get_playoff_teams(simmed)
        
        for team in playoff_teams:
            team_index = df.index[df['name'] == team][0]
            
            df.at[team_index, 'playoff'] += 1
            
    for index, row in df.iterrows():
        df.at[index, 'playoff'] /= runs
    
    print("Time Taken", time.time() - start)
    return df
    
def get_playoff_teams(new_df):
    
    df = new_df.copy(deep=True)
    
    #split dataframe into smaller sets of teams
    east = rank_teams(df[df['conference'] == 'Eastern'])
    west = rank_teams(df[df['conference'] == 'Western'])
    
    atlantic = rank_teams(df[df['division'] == 'Atlantic'])
    metro = rank_teams(df[df['division'] == 'Metropolitan'])
    pacific = rank_teams(df[df['division'] == 'Pacific'])
    central = rank_teams(df[df['division'] == 'Central'])
    
    
    #initialize lists to store playoff teams
    atl_teams = []
    met_teams = []
    ewc_teams = []
    
    cen_teams = []
    pac_teams = []
    wwc_teams = []
    
    #Add top teams from eastern divisions
    count = 0
    for row in atlantic.values.tolist():
        atl_teams.append(row[0])
        count += 1 
        if count > 2:
            break
        
    count = 0
    for row in metro.values.tolist():
        met_teams.append(row[0])
        count += 1 
        if count > 2:
            break
        
    #Get wildcard teams from east
    count = 0
    for row in east.values.tolist():
        if (row[0] not in atl_teams) and (row[0] not in met_teams):
            ewc_teams.append(row[0])
            count += 1 
            if count > 1:
                break
            
    #Add top teams from western divisions
    count = 0
    for row in pacific.values.tolist():
        pac_teams.append(row[0])
        count += 1 
        if count > 2:
            break
    
    count = 0
    for row in central.values.tolist():
        cen_teams.append(row[0])
        count += 1 
        if count > 2:
            break
        
    #Get wildcard teams from west
    count = 0
    for row in west.values.tolist():
        if (row[0] not in cen_teams) and (row[0] not in pac_teams):
            wwc_teams.append(row[0])
            count += 1 
            if count > 1:
                break
    
    return atl_teams + met_teams + ewc_teams + pac_teams + cen_teams + wwc_teams


'''
Ranks teams passed in order based on points and tiebreakers
'''    
def rank_teams(df):
    return df.sort_values(by = ['points', 'played', 'rw', 'row', 'wins', 'goalsFor'], 
                        ascending = [False, False, False, False, False, False], ignore_index = True)

'''
Returns every team and their place in the standings as of the specified time.
'''
def get_old_standings(year, month, day):
    
    df = initialize_dataframe()
    
    if month > 8: 
        start = year
    else:
        start = year - 1
    
    
    #Get past data from API
    response_past = requests.get(API_URL + "/api/v1/schedule?startDate=" + str(start) + "-8-1&endDate=" 
                            + str(year) + "-" + str(month) + "-" + str(day), 
                            params={"Content-Type": "application/json"})
    data_past = response_past.json()
    
    
    df = calculate_standings(data_past, df) 
    
    sched = get_schedule(year, month, day)

                
    return df, sched


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
    for date in data_future["dates"]:
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


temp, schedule = get_old_standings(2022, 10, 10)

t = get_playoff_odds(temp, schedule)

print(t)