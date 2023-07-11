from django.http import HttpResponse
from django.template import loader
from django.core.paginator import Paginator

from .models import Player, Season, Stats
from .players import reset_data, get_fantasy_points
from .forms import InputForm, FantasyScoring

from django.core.exceptions import *

def player_page(request):
    
    #Reload stats if needed. Mostly used for debugging or production
    reload_players = False
    if reload_players:
        reset_data() 
    
    #Process the request and get information
    player_list, sort_column, sort_direction, form, fant = process_request(request)
    
    #Create pages
    paginator = Paginator(player_list, 50)
    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)
    
    #Collect data to send to template
    context = {
        "player_list": page,
        "sort_column": sort_column,
        "sort_direction": sort_direction,
        "page_number": page_number,
        "form": form,
        "fant": fant
    }
    
    #Load template
    template = loader.get_template("players.html")
    return HttpResponse(template.render(context, request))


#Process the request that the player page recieves
def process_request(request):
    #If the request comes from the "filter" method in the html
    #Add filters to position or team
    team = 'all'
    position = 'all'
    season = 'all'
    if request.method == 'POST':
        
        #Gather filter form data
        season = request.POST.get('year', 'all')
        team = request.POST.get('team', 'all')
        position = request.POST.get('position', 'all') 
        form = InputForm(initial={'year':season, 'team':team, 'position':position})
        
        #Gather fantasy form data
        fantasyData = {
            'games': request.POST.get('games', 0),
            'goals': request.POST.get('goals', 0),
            'assists': request.POST.get('assist', 0),
            'points': request.POST.get('points', 0),
            'plusMinus': request.POST.get('plusMinus', 0),
            'pim': request.POST.get('pim', 0),
            'ppp': request.POST.get('ppp', 0),
            'shp': request.POST.get('shp', 0),
            'shots': request.POST.get('shots', 0),
            'hits': request.POST.get('hits', 0),
            'blocks': request.POST.get('blocks', 0),
            'shifts': request.POST.get('shifts', 0),
            'gwg': request.POST.get('gwg', 0),
            'otg': request.POST.get('otg', 0)
        }
        fant = FantasyScoring(initial=fantasyData)
        
        
        if 'fantasy_submit' in request.POST:
            get_fantasy_points(fantasyData)
            
    else:
        form = InputForm()
        fant = FantasyScoring()
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
    
    return player_list, sort_column, sort_direction, form, fant