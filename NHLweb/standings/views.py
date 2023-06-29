from django.http import HttpResponse
from django.template import loader

from .models import Team

from .teams import reload_teams
from .odds import reset_odds

def home(request):
    
    reload_standings = True
    reload_graph = True
    
    #Reloads standing if needed
    if reload_standings:
        reload_teams()
        
    if reload_graph:
        reset_odds()

    #Retrieve all teams and order them by points.
    team_list = Team.objects.order_by("-points")
    
    template = loader.get_template("league.html")
    
    context = {
        "team_list": team_list,
        }
    
    return HttpResponse(template.render(context, request))

    
    