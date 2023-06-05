from django.http import HttpResponse
from django.template import loader

from .models import Team, Odds

from .tools import reload_teams

def home(request):
    
    reload = True
    
    #Reloads standing if needed
    if reload:
        reload_teams()


    #Retrieve all teams and order them by points.
    team_list = Team.objects.order_by("-points")
    
    template = loader.get_template("standings/league.html")
    
    context = {
        "team_list": team_list,
        }
    
    
    return HttpResponse(template.render(context, request))
    
    
    