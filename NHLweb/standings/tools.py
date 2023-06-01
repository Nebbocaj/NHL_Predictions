import requests
import pandas as pd
import random

from .historic_data import get_old_standings

API_URL = "https://statsapi.web.nhl.com"

'''
Returns every team and their current place in the standings
'''
def get_teams():
    
    response = requests.get(API_URL + "/api/v1/standings", params={"Content-Type": "application/json"})
    data = response.json()
    
    team_list = []
    
    for div in range(4):
        division = data["records"][div]["division"]["name"]
        conference = data["records"][div]["conference"]["name"]
        for i in range(8):
            w = data["records"][div]["teamRecords"][i]["leagueRecord"]["wins"]
            l = data["records"][div]["teamRecords"][i]["leagueRecord"]["losses"]
            otl = data["records"][div]["teamRecords"][i]["leagueRecord"]["ot"]
            
            team_list.append([data["records"][div]["teamRecords"][i]["team"]["name"],
                              conference, division, w+l+otl, w, l, otl,
                              data["records"][div]["teamRecords"][i]["points"],
                              data["records"][div]["teamRecords"][i]["regulationWins"],
                              data["records"][div]["teamRecords"][i]["row"],
                              data["records"][div]["teamRecords"][i]["goalsScored"],
                              data["records"][div]["teamRecords"][i]["goalsAgainst"], 0])
            
    labels = ['name', 'conference', 'division', 'played', 'wins', 'losses', 'otl', 'points',  'rw', 'row', 'goalsFor', 'goalsAgainst', 'playoff']
    
    df = pd.DataFrame(team_list, columns = labels)
    
    
    
    return df


                  
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

'''
takes standings and runs simulations.
returns playoff odds for each team
'''
def get_playoff_odds(df, schedule, runs = 100):
    
    df = df.copy(deep=True)
    
    for i in range(100):
        simmed = simulate_season(df, schedule)
    
        playoff_teams = get_playoff_teams(simmed)
        
        for team in playoff_teams:
            team_index = df.index[df['name'] == team][0]
            
            df.at[team_index, 'playoff'] += 1
    
    results = []
    for row in df.values.tolist():
        results.append([row[0], round(row[-1] / runs,2)])
        
    print(results)
    
    return results
    
        


'''
returns the 16 teams that make the playoffs
'''
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
    

# temp, schedule = historic_data.get_old_standings(2023, 4, 1)

# t = get_playoff_odds(temp, schedule)


