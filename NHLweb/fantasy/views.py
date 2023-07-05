from django.http import HttpResponse
from django.template import loader
from django.core.paginator import Paginator

from .models import Player, Season, Stats
from .players import reset_data

def player_page(request):
    
    reload_players = False
    if reload_players:
        reset_data()
        
    sort_column = request.GET.get('sort', 'goals')
    sort_direction = request.GET.get('dir', 'desc')
    
        
    if sort_direction == 'desc':
        prefix = "-"
    else:
        prefix = ""
        
    player_list = Stats.objects.filter(season__year=2023).order_by(f"{prefix}{sort_column}")
    
    
    paginator = Paginator(player_list, 50)
    page_number = request.GET.get('page', 1)
    
    page = paginator.get_page(page_number)
        
    print(sort_column, sort_direction)
    context = {
        "player_list": page,
        "sort_column": sort_column,
        "sort_direction": sort_direction,
        "page_number": page_number,
    }
    
    template = loader.get_template("players.html")
    return HttpResponse(template.render(context, request))
