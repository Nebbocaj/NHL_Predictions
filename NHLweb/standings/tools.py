import requests
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
    
    response = requests.get(API_URL + "/schedule?startDate=2021-07-31&endDate=2021-10-31", params={"Content-Type": "application/json"})
    data = response.json()
    
    for date in data["dates"]:
        print("--- Date:", date["date"])
        
        for game in date["games"]:
            print(".", game["teams"]["away"]["team"]["name"], "﹒", game["teams"]["home"]["team"]["name"], 
                  "/", f"{game['teams']['away']['score']}:{game['teams']['home']['score']}", "/", game["status"]["detailedState"])
    
get_old_standings(2023, 5, 28)