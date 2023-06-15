import requests
from datetime import date, timedelta

from .models import Team, Odds
from .historic_data import get_schedule, initialize_dataframe, calculate_standings
from .teams import get_playoff_odds


API_URL = "https://statsapi.web.nhl.com"

'''
resets the odds table from scratch
'''
def reset_odds():
    
    #Collect and delete all rows
    all_odds = Odds.objects.all()
    all_odds.delete()
    
    #Initialize a row for each team in the table
    team_list = Team.objects.order_by("-points")
    for t in team_list:
        new_odds = Odds(name = t.name)
        new_odds.save()
        
    #Get the series of dates between the start of the season and the current date
    today = str(date.today())
    y = int(today[:4])
    m = int(today[5:7])
    d = int(today[8:10])
    opening, closing = season_date_params(y, m, d)
    all_dates = get_dates(opening, closing)
    
    #Initialize a new dataframe
    old_standings = initialize_dataframe()    
    
    #Loop through all days in the list
    for day in all_dates:
        
        print(day)
        
        y1 = str(day)[:4]
        m1 = str(day)[5:7]
        d1 = str(day)[8:10]
        
        #Get game data from that specific day
        '''look into speeding this section up ****************************'''
        response_past = requests.get(API_URL + "/api/v1/schedule?startDate=" + y1 + "-" + m1 + "-" + d1 + "&endDate=" 
                                + y1 + "-" + m1 + "-" + d1, 
                                params={"Content-Type": "application/json"})
        data_past = response_past.json()
        
        #Update the datafraem with the new information from the games of the day
        old_standings = calculate_standings(data_past, old_standings)
        
        #Get the schedule from day onward
        old_schedule = get_schedule(int(y1), int(m1), int(d1))
        '''**************************************************************'''
        
        #Calculate the playoff odds for each team given the standings
        updated = get_playoff_odds(old_standings, old_schedule, runs = 1000)
        
        #Update the data table with new odds information
        for index, row in updated.iterrows():
            team_name = updated.at[index, 'name']
            team_odds = updated.at[index, 'playoff']
            
            team_object = Odds.objects.filter(name = team_name)[0]
            
            previous_odds = team_object.get_values()
            if previous_odds == [-1]:
                team_object.set_values([team_odds])
            else:
                previous_odds.append(float(team_odds))
                team_object.set_values(previous_odds)
                
            team_object.save()
                
        print(updated)
        #print(updated)
        
        
'''
Gets the first and last day of the regular season.
Used to determine where to start calculating odds.
'''
def season_date_params(year, month, day):
    
    if month > 8: 
        start = year
    else:
        start = year - 1
    
    #Get past data from API
    response_past = requests.get(API_URL + "/api/v1/schedule?startDate=" + str(start) + "-8-1&endDate=" 
                            + str(year) + "-" + str(month) + "-" + str(day), 
                            params={"Content-Type": "application/json"})
    season_data = response_past.json()

    return get_open(year, month, day, season_data), get_close(year, month, day, season_data)

'''
Get the date of the opening game for the season
'''
def get_open(year, month, day, season_data):
    for d in season_data["dates"][1:]:
        for game in d["games"]:
            if game['gameType'] == 'R':
                return d['date']
                
    return str(year) + "-" + str(month) + "-" + str(day)
    
'''
Get the data for the last day of the regular season
'''
def get_close(year, month, day, season_data):
    for d in season_data["dates"][::-1]:
        for game in d["games"]:
            if game['gameType'] == 'R':
                return d['date']
                
    return str(year) + "-" + str(month) + "-" + str(day)

'''
return all dates in between two points.
Used in collecting old data when odds are reset.
'''
def get_dates(start, end):
    start_date = date(int(start[:4]), int(start[5:7]), int(start[8:10]))
    end_date = date(int(end[:4]), int(end[5:7]), int(end[8:10]))
    delta = timedelta(days=1)
    dates = []

    while start_date <= end_date:
        dates.append(start_date)
        start_date += delta

    return dates