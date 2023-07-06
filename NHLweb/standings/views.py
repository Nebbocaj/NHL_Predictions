from django.http import HttpResponse
from django.template import loader

from .models import Team

from .teams import reload_teams
from .odds import reset_odds

def team_odds(request):
    
    reload_standings = False
    reload_graph = False
    
    #Reloads standing if needed
    if reload_standings:
        reload_teams()
        
    if reload_graph:
        reset_odds()
        
    #Determine how the data should be sorted
    sort_column = request.GET.get('sort', 'points')
    sort_direction = request.GET.get('dir', 'desc')
    
    #Get the sorting prefix for descending of ascending order
    if sort_direction == 'desc':
        prefix = "-"
    else:
        prefix = ""

    #Retrieve all teams and order them by points.
    team_list = Team.objects.order_by(f"{prefix}{sort_column}")
    
    template = loader.get_template("team_odds.html")
    
    context = {
        "team_list": team_list,
        "sort_column": sort_column,
        "sort_direction": sort_direction,
        }
    
    return HttpResponse(template.render(context, request))


def team_standings(request):
    
    reload_standings = False
    reload_graph = False
    
    #Reloads standing if needed
    if reload_standings:
        reload_teams()
        
    if reload_graph:
        reset_odds()
        
    #Determine how the data should be sorted
    sort_column = request.GET.get('sort', 'points')
    sort_direction = request.GET.get('dir', 'desc')
    
    #Get the sorting prefix for descending of ascending order
    if sort_direction == 'desc':
        prefix = "-"
    else:
        prefix = ""

    #Retrieve all teams and order them by points.
    team_list = Team.objects.order_by(f"{prefix}{sort_column}")
    
    template = loader.get_template("team_standings.html")
    
    context = {
        "team_list": team_list,
        "sort_column": sort_column,
        "sort_direction": sort_direction,
        }
    
    return HttpResponse(template.render(context, request))

    
    