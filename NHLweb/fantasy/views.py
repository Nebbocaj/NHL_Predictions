from django.http import HttpResponse
from django.template import loader

from .models import Player, Season, Stats
from .players import reset_data

def player_page(request):
    
    reload_players = True
    if reload_players:
        reset_data()
        
    player_list = Stats.objects.order_by("-goals")
        
    context = {
        "player_list": player_list
        } 
    template = loader.get_template("players.html")
    return HttpResponse(template.render(context, request))
