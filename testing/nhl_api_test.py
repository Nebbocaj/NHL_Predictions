import requests
import json

API_URL = "https://statsapi.web.nhl.com/api/v1"
    
response = requests.get(API_URL + "/schedule?startDate=2023-05-20&endDate=2023-07-22", params={"Content-Type": "application/json"})
data = response.json()


# for date in data["dates"]:
#     print("--- Date:", date["date"])
#     # and now through games
#     for game in date["games"]:
#         print(".", game["teams"]["away"]["team"]["name"], "﹒", game["teams"]["home"]["team"]["name"], "/", f"{game['teams']['away']['score']}:{game['teams']['home']['score']}", "/", game["status"]["detailedState"])
        
response = requests.get(API_URL + "/standings", params={"Content-Type": "application/json"})
data = response.json()

print(json.dumps(data["records"][3]["teamRecords"][0], indent = 1))

for div in range(4):
    for i in range(8):
        
        print(data["records"][div]["teamRecords"][i]["team"]["name"],
              data["records"][div]["teamRecords"][i]["leagueRecord"]["wins"],
              data["records"][div]["teamRecords"][i]["leagueRecord"]["losses"],
              data["records"][div]["teamRecords"][i]["leagueRecord"]["ot"],
              data["records"][div]["teamRecords"][i]["points"],
              data["records"][div]["teamRecords"][i]["regulationWins"],
              data["records"][div]["teamRecords"][i]["row"],
              data["records"][div]["teamRecords"][i]["goalsScored"],
              data["records"][div]["teamRecords"][i]["goalsAgainst"],
              data["records"][div]["teamRecords"][i]["goalsScored"] - data["records"][div]["teamRecords"][i]["goalsAgainst"])