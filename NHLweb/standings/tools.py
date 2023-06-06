import requests
import pandas as pd
import numpy as np
from datetime import date

from .historic_data import get_old_standings, get_schedule
#import historic_data
from .models import Team

API_URL = "https://statsapi.web.nhl.com"


'''
Retrieve all teams from the NHL api from scratch if needed
This will be done once per day as it can take a bit to simulate
The point expectations for teams
'''
def reload_teams():
    
    #Collect and delete all rows
    all_teams = Team.objects.all()
    all_teams.delete()
    
    #Get a pandas dataframe of all teams
    team_standings = get_teams()
    
    #Convert the standings into rows in the database
    for index, team in team_standings.iterrows():
        
        gp = team['played']
        w = team['wins']
        l = team['losses']
        otl = team['otl']
        
        new_team = Team(name = team['name'], played = gp, wins = w, losses = l,
                        otl = otl, points = team['points'],
                        pointPer = round((2*w + otl) / (2*gp), 3), 
                        rw = team['rw'], row = team['row'],
                        goalsFor = team['goalsFor'], goalsAgainst = team['goalsAgainst'],
                        goalDiff = team['goalsFor'] - team['goalsAgainst'],
                        playoffOdds = team['playoff'])

        new_team.save()


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

    today = str(date.today())
    schedule = get_schedule(int(today[:4]), int(today[5:7]), int(today[8:10]))
    
    df = get_playoff_odds(df, schedule)

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
    
    #build a series of random events
    num_games = len(schedule)
    type_events = np.random.uniform(0, 1, num_games)
    win_events = np.random.uniform(0, 1, num_games)
    
    #Split the games into a list of home and away teams
    home_teams = np.array([game[1] for game in schedule])
    away_teams = np.array([game[0] for game in schedule])
    
    #Create basic masks for events
    so_mask = type_events <= so_odds
    ot_mask = (type_events <= ot_odds) & (type_events > so_odds)
    reg_mask = type_events > ot_odds
    home_mask = win_events <= home_win
    away_mask = win_events > home_win

    #Create more complex masks for dual events
    home_so_mask = home_mask & so_mask
    home_ot_mask = home_mask & ot_mask
    home_reg_mask = home_mask & reg_mask
    away_so_mask = away_mask & so_mask
    away_ot_mask = away_mask & ot_mask
    away_reg_mask = away_mask & reg_mask
    
    #Create final masks for calculating wins, otls, and losses
    home_win_mask = home_so_mask | home_ot_mask | home_reg_mask
    away_win_mask = away_so_mask | away_ot_mask | away_reg_mask
    home_otl_mask = home_so_mask | home_ot_mask
    away_otl_mask = away_so_mask | away_ot_mask
    home_row_mask = home_reg_mask | home_ot_mask
    away_row_mask = away_reg_mask | away_ot_mask
    
    #Add all wins to data
    win_counts = pd.Series(home_teams[home_win_mask]).value_counts() + \
        pd.Series(away_teams[away_win_mask]).value_counts()
    df['wins'] += df['name'].map(win_counts).fillna(0)
    
    #Add all losses to data
    loss_counts = pd.Series(home_teams[away_reg_mask]).value_counts() + \
        pd.Series(away_teams[home_reg_mask]).value_counts()
    df['losses'] += df['name'].map(loss_counts).fillna(0)
    
    #Add all otls to data
    otl_counts = pd.Series(home_teams[away_otl_mask]).value_counts() + \
        pd.Series(away_teams[home_otl_mask]).value_counts()
    df['otl'] += df['name'].map(otl_counts).fillna(0)
    
    #Add all rws to data
    rw_counts = pd.Series(home_teams[home_reg_mask]).value_counts() + \
        pd.Series(away_teams[away_reg_mask]).value_counts()
    df['rw'] += df['name'].map(rw_counts).fillna(0)
    
    #Add all rows to data
    row_counts = pd.Series(home_teams[home_row_mask]).value_counts() + \
        pd.Series(away_teams[away_row_mask]).value_counts()
    df['row'] += df['name'].map(row_counts).fillna(0)
    
    #Get points for each team
    df['points'] = 2 * df['wins'] + df['otl']
    
    #Get games played for each team
    df['played'] += df['wins'] + df['losses'] + df['otl']
    
    return df

'''
takes standings and runs simulations.
returns playoff odds for each team
'''
def get_playoff_odds(df, schedule, runs = 100):
    
    df = df.copy(deep=True)
    
    for i in range(runs):
        print(i)
        simmed = simulate_season(df, schedule)
    
        playoff_teams = get_playoff_teams(simmed)
        
        for team in playoff_teams:
            team_index = df.index[df['name'] == team][0]
            
            df.at[team_index, 'playoff'] += 1
            
    for index, row in df.iterrows():
        df.at[index, 'playoff'] /= runs
    
    return df
    
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
    

#temp, schedule = historic_data.get_old_standings(2022, 10, 30)

#t = get_playoff_odds(temp, schedule)


