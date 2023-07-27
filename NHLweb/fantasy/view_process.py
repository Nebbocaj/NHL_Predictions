from .forms import InputForm, FantasyScoring, GoalieInputForm, GoalieFantasyScoring
from .models import Player, Stats, GoalieStats
from .players import get_fantasy_points, get_fantasy_goalie_points
from django.core.exceptions import *

#Process the request that the player page recieves
def process_player_request(request):
    #If the request comes from the "filter" method in the html
    #Add filters to position or team
    team = 'all'
    position = 'all'
    season = '2023'
    if request.method == 'POST':
        
        #Gather filter form data
        season = request.POST.get('year', 'all')
        team = request.POST.get('team', 'all')
        position = request.POST.get('position', 'all') 
        form = InputForm(initial={'year':season, 'team':team, 'position':position})
            
    else:
        form = InputForm()

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
    
    players = Player.objects.all()


    #Update fantasy points
    if request.method == 'POST':
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

        player_list = get_fantasy_points(player_list, fantasyData)
    else:
        player_list = get_fantasy_points(player_list)
        fant = FantasyScoring()

    
    return players, player_list, sort_column, sort_direction, form, fant

#Process the request that the player page recieves
def process_goalie_request(request):
    #If the request comes from the "filter" method in the html
    #Add filters to position or team
    team = 'all'
    season = '2023'
    if request.method == 'POST':
        
        #Gather filter form data
        season = request.POST.get('year', 'all')
        team = request.POST.get('team', 'all')
        form = GoalieInputForm(initial={'year':season, 'team':team})
            
    else:
        form = GoalieInputForm()

    #Determine how the data should be sorted
    sort_column = request.GET.get('sort', 'fantasyPoints')
    sort_direction = request.GET.get('dir', 'desc')
    
    #Set the sort direction based on input
    if sort_direction == 'desc':
        prefix = "-"
    else:
        prefix = ""
    
    
    #Get all stat objects that satisfy the specified filters.
    player_list = GoalieStats.objects.all()
    
    if season != 'all':
        player_list = player_list.filter(season__year=int(season))

    if team != 'all':
        player_list = player_list.filter(team__acronym=team)
    
    player_list = player_list.order_by(f"{prefix}{sort_column}")
    
    players = Player.objects.all()


    if request.method == 'POST':
        #Gather fantasy form data
        fantasyData = {
            'games': request.POST.get('games', 0),
            'wins': request.POST.get('wins', 0),
            'losses': request.POST.get('losses', 0),
            'otl': request.POST.get('otl', 0), 
            'shutouts': request.POST.get('shutouts', 0),
            'saves': request.POST.get('saves', 0),
            'goalsAgainst' : request.POST.get('goalsAgainst', 0),
        }
        fant = GoalieFantasyScoring(initial=fantasyData)

        get_fantasy_goalie_points(player_list, fantasyData)
    else:
        fant = GoalieFantasyScoring()
        get_fantasy_goalie_points(player_list)
    
    return players, player_list, sort_column, sort_direction, form, fant