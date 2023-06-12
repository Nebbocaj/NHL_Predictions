import requests
import pandas as pd
import numpy as np
from datetime import date, timedelta


from .historic_data import get_old_standings, get_schedule
#import historic_data
from .models import Team, Odds

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
                        playoffOdds = team['playoff'], presidentOdds = team['president'], 
                        conferenceOdds = team['conf%'], divisionOdds = team['div1'], 
                        div2Odds = team['div2'], div3Odds = team['div3'],
                        wc1Odds = team['wc1'], wc2Odds = team['wc2'])

        new_team.save()


def reset_odds():
    
    #Collect and delete all rows
    all_odds = Odds.objects.all()
    all_odds.delete()
    
    team_list = Team.objects.order_by("-points")
    
    for t in team_list:
        new_odds = Odds(name = t.name)
        new_odds.save()
    
    all_dates = get_dates()
        
    

'''
return all dates in between two points.
Used in collecting old data when odds are reset.
'''
def get_dates():
    start_date = date(2022, 7, 1)
    end_date = date(2023, 6, 1)
    delta = timedelta(days=1)
    dates = []

    while start_date <= end_date:
        dates.append(start_date)
        start_date += delta

    return dates
        
        
    

'''
Returns every team and their current place in the standings
'''
def get_teams():
    
    response = requests.get(API_URL + "/api/v1/standings", params={"Content-Type": "application/json"})
    data = response.json()
    team_list = []
    
    #Initialize a 2D list with current standings information
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
                              data["records"][div]["teamRecords"][i]["goalsAgainst"], 0, 
                              0,0,0,0,0,0,0])
    
    #Turn the list into a pandas dataframe
    labels = ['name', 'conference', 'division', 'played', 'wins', 'losses', 
              'otl', 'points',  'rw', 'row', 'goalsFor', 'goalsAgainst', 'playoff',
              'president', 'conf%', 'div1', 'div2', 'div3', 'wc1', 'wc2']
    df = pd.DataFrame(team_list, columns = labels)

    #Get the schedule for all teams
    today = str(date.today())
    schedule = get_schedule(int(today[:4]), int(today[5:7]), int(today[8:10]))
    
    #Update the dataframe with data from the simmed season
    df = get_playoff_odds(df, schedule)

    return df

'''
takes standings and runs simulations.
returns playoff odds for each team
'''
def get_playoff_odds(df, schedule, runs = 5):
    
    df = df.copy(deep=True)
    
    for i in range(runs):
        simmed = simulate_season(df, schedule)
        
        #retrieve all playoff team information and winners from the simmed season
        playoffs, pres_win, east_win, west_win, atl_teams, met_teams, \
                ewc_teams, pac_teams, cen_teams, wwc_teams = get_playoff_teams(simmed)
        
        #For each team in the playoffs, add 1 playoff appearence to the database
        for team in playoffs:
            team_index = df.index[df['name'] == team][0]
            df.at[team_index, 'playoff'] += 1
            
        #Update president winner score
        pres_index = df.index[df['name'] == pres_win][0]
        df.at[pres_index, 'president'] += 1
        
        #Update conference winners' scores
        conf1_index = df.index[df['name'] == east_win][0]
        conf2_index = df.index[df['name'] == west_win][0]
        df.at[conf1_index, 'conf%'] += 1
        df.at[conf2_index, 'conf%'] += 1
        
        #Update div winner scores
        atl_index1 = df.index[df['name'] == atl_teams[0]][0]
        met_index1 = df.index[df['name'] == met_teams[0]][0]
        pac_index1 = df.index[df['name'] == pac_teams[0]][0]
        cen_index1 = df.index[df['name'] == cen_teams[0]][0]
        df.at[atl_index1, 'div1'] += 1
        df.at[met_index1, 'div1'] += 1
        df.at[pac_index1, 'div1'] += 1
        df.at[cen_index1, 'div1'] += 1
        
        #Update div second place scores
        atl_index2 = df.index[df['name'] == atl_teams[1]][0]
        met_index2 = df.index[df['name'] == met_teams[1]][0]
        pac_index2 = df.index[df['name'] == pac_teams[1]][0]
        cen_index2 = df.index[df['name'] == cen_teams[1]][0]
        df.at[atl_index2, 'div2'] += 1
        df.at[met_index2, 'div2'] += 1
        df.at[pac_index2, 'div2'] += 1
        df.at[cen_index2, 'div2'] += 1
        
        #Update div third place scores
        atl_index3 = df.index[df['name'] == atl_teams[2]][0]
        met_index3 = df.index[df['name'] == met_teams[2]][0]
        pac_index3 = df.index[df['name'] == pac_teams[2]][0]
        cen_index3 = df.index[df['name'] == cen_teams[2]][0]
        df.at[atl_index3, 'div3'] += 1
        df.at[met_index3, 'div3'] += 1
        df.at[pac_index3, 'div3'] += 1
        df.at[cen_index3, 'div3'] += 1
        
        #Update wc1 scores
        ewc_index1 = df.index[df['name'] == ewc_teams[0]][0]
        wwc_index1 = df.index[df['name'] == wwc_teams[0]][0]
        df.at[ewc_index1, 'wc1'] += 1
        df.at[wwc_index1, 'wc1'] += 1
        
        #Update wc2 scores
        ewc_index2 = df.index[df['name'] == ewc_teams[1]][0]
        wwc_index2 = df.index[df['name'] == wwc_teams[1]][0]
        df.at[ewc_index2, 'wc2'] += 1
        df.at[wwc_index2, 'wc2'] += 1
        
            
    for index, row in df.iterrows():
        df.at[index, 'playoff'] *= 100 / runs
        df.at[index, 'president'] *= 100 / runs 
        df.at[index, 'conf%'] *= 100 / runs 
        df.at[index, 'div1'] *= 100 / runs
        df.at[index, 'div2'] *= 100 / runs 
        df.at[index, 'div3'] *= 100 / runs 
        df.at[index, 'wc1'] *= 100 / runs 
        df.at[index, 'wc2'] *= 100 / runs 
    
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
returns the 16 teams that make the playoffs,
as well as the presidents winner and conference winners.
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
    
    total = rank_teams(df)
    
    
    #initialize lists to store playoff teams
    atl_teams = []
    met_teams = []
    ewc_teams = []
    
    cen_teams = []
    pac_teams = []
    wwc_teams = []
    
    #get the champions of the league, and each conference
    pres_win = total.values.tolist()[0][0]
    east_win = east.values.tolist()[0][0]
    west_win = west.values.tolist()[0][0]
    
    
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
            
    #Get a list of the 16 teams that make the playoffs
    playoffs = atl_teams + met_teams + ewc_teams + pac_teams + cen_teams + wwc_teams
    
    return playoffs, pres_win, east_win, west_win, atl_teams, met_teams, \
            ewc_teams, pac_teams, cen_teams, wwc_teams


'''
Ranks teams passed in order based on points and tiebreakers
'''    
def rank_teams(df):
    return df.sort_values(by = ['points', 'played', 'rw', 'row', 'wins', 'goalsFor'], 
                        ascending = [False, False, False, False, False, False], ignore_index = True)
    

#temp, schedule = historic_data.get_old_standings(2022, 10, 30)

#t = get_playoff_odds(temp, schedule)


