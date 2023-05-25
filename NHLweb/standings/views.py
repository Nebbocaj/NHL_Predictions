from django.http import HttpResponse
from django.template import loader

from .models import Team

from .tools import get_teams

def home(request):
    
    all_teams = Team.objects.all()
    
    #Make sure that there are exactly 32 teams at all times.
    if len(all_teams) != 32:
        all_teams.delete()
        for t in get_teams():
            new_team = Team(name = t[0], points = t[1])
            new_team.save()
            
    #Retrieve all teams and order them by points.
    #THIS WILL CHANGE LATER WHEN THERE IS A BETTER ORGANIZATION SYSTEM
    team_list = Team.objects.order_by("-points")
    
    template = loader.get_template("standings/league.html")
    
    context = {
        "team_list": team_list,
        }
    
    return HttpResponse(template.render(context, request))
    
    
    
    # output = ", ".join([str(q.name) + " " +  str(q.points) for q in team_list])
    
    # return HttpResponse(output)