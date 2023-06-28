from django.http import HttpResponse
from django.template import loader

from .models import Player, Season, Stats
from .players import update_players

def player_page(request):
    
    reload_players = True
    if reload_players:
        update_players()
        
    player_list = Stats.objects.order_by("-goals")
        
    context = {
        "player_list": player_list
        }
    print(context)    
    template = loader.get_template("players.html")
    return HttpResponse(template.render(context, request))
