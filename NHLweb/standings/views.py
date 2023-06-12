from django.http import HttpResponse
from django.template import loader

from .models import Team, Odds

from .tools import reload_teams, reset_odds

def home(request):
    
    reload_standings = True
    
    #Reloads standing if needed
    if reload_standings:
        reload_teams()


    #Retrieve all teams and order them by points.
    team_list = Team.objects.order_by("-points")
    
    template = loader.get_template("standings/league.html")
    
    context = {
        "team_list": team_list,
        }
    
    
    reload_graph = True
    
    if reload_graph:
        reset_odds()
    
    return HttpResponse(template.render(context, request))
    
    
    