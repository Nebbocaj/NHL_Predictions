import requests
import json

API_URL = "https://statsapi.web.nhl.com/api/v1"
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