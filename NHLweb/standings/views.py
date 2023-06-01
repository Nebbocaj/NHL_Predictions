from django.http import HttpResponse
from django.template import loader

from .models import Team

from .tools import get_teams

def home(request):
    
    all_teams = Team.objects.all()
    
    #Make sure that there are exactly 32 teams at all times.
    #if len(all_teams) != 32:
    all_teams.delete()
    
    team_standings = get_teams()
    
    print(team_standings.to_string())
    
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

    #Retrieve all teams and order them by points.
    team_list = Team.objects.order_by("-points")
    
    template = loader.get_template("standings/league.html")
    
    context = {
        "team_list": team_list,
        }
    
    return HttpResponse(template.render(context, request))
    
    
    
    # output = ", ".join([str(q.name) + " " +  str(q.points) for q in team_list])
    
    # return HttpResponse(output)