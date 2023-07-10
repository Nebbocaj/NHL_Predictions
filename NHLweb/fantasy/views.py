from django.http import HttpResponse
from django.template import loader
from django.core.paginator import Paginator

from .models import Player, Season, Stats
from .players import reset_data, get_fantasy_points
from .forms import InputForm

from django.core.exceptions import *

def player_page(request):
    
    form = InputForm()
    
    #If the request comes from the "filter" method in the html
    #Add filters to position or team
    team = 'all'
    position = 'all'
    season = 'all'
    if request.method == 'POST':
        season = request.POST.get('year', 'all')
        team = request.POST.get('team', 'all')
        position = request.POST.get('position', 'all') 

    #Reload stats if needed. Mostly used for debugging or production
    reload_players = False
    reset_points = False
    if reload_players:
        reset_data() 
    if reset_points:
        get_fantasy_points()
        
    #Determine how the data should be sorted
    sort_column = request.GET.get('sort', 'fantasyPoints')
    sort_direction = request.GET.get('dir', 'desc')
    
    #Set the sort direction based on input
    if sort_direction == 'desc':
        prefix = "-"
    else:
        prefix = ""
    
    
    #Get all stat objects that satisfy the specified filters.
    player_list = Stats.objects.all()
    
    if season != 'all':
        player_list = player_list.filter(season__year=int(season))

    if team != 'all':
        player_list = player_list.filter(team__acronym=team)
    
    if position != 'all':
        player_list = player_list.filter(player__pos_code=position)
    
    player_list = player_list.order_by(f"{prefix}{sort_column}")
    
    #Create pages
    paginator = Paginator(player_list, 50)
    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)
        
    form = InputForm(initial={'year':season, 'team':team, 'position':position})
    
    context = {
        "player_list": page,
        "sort_column": sort_column,
        "sort_direction": sort_direction,
        "page_number": page_number,
        "form": form,
    }
    
    template = loader.get_template("players.html")
    return HttpResponse(template.render(context, request))