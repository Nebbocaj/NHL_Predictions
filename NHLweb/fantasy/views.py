from django.http import HttpResponse
from django.template import loader
from django.core.paginator import Paginator

from .players import reset_data

from .models import Player, Season, Stats, GoalieStats

from .view_process import process_player_request, process_goalie_request

RELOAD_PLAYERS = False

#View function for the player page
def player_page(request):
    
    #Reload stats if needed. Mostly used for debugging or production
    if RELOAD_PLAYERS:
        reset_data() 
    
    #Process the request and get information
    player_list, sort_column, sort_direction, form, fant = process_player_request(request)
    
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


def player_details(request, id_num):
    
    person = Player.objects.filter(id_num=id_num)[0]
    details = Stats.objects.filter(player=person)
    
    context = {
        "player_list": details
        }
    
    template = loader.get_template("players_details.html")
    return HttpResponse(template.render(context, request))

def goalie_details(request, id_num):
    
    person = Player.objects.filter(id_num=id_num)[0]
    details = GoalieStats.objects.filter(player=person)
    
    context = {
        "player_list": details
        }
    
    template = loader.get_template("goalies_details.html")
    return HttpResponse(template.render(context, request))

#View function for the goalie page
def goalie_page(request):
    
    #Reload stats if needed. Mostly used for debugging or production
    if RELOAD_PLAYERS:
        reset_data() 
    
    #Process the request and get information
    player_list, sort_column, sort_direction, form, fant = process_goalie_request(request)
    
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
    template = loader.get_template("goalies.html")
    return HttpResponse(template.render(context, request))

