from django.http import HttpResponse
from django.template import loader
from django.core.paginator import Paginator

from .players import reset_data

from django.shortcuts import render, redirect
from django.urls import reverse

from .models import Player, Season, Stats, GoalieStats

from .view_process import process_player_request, process_goalie_request

RELOAD_PLAYERS = False

#View function for the player page
def player_page(request):
    
    #Reload stats if needed. Mostly used for debugging or production
    if RELOAD_PLAYERS:
        reset_data() 
    
    #Process the request and get information
    players, player_list, sort_column, sort_direction, form, fant = process_player_request(request)
    
    #Create pages
    paginator = Paginator(player_list, 50)
    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)
    
    #Collect data to send to template
    context = {
        "players": players,
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
    

#Get the player detail page that shows player stats
def player_details(request, id_num):
    
    #If this is gotten to by search, handle the inputs and redirect to proper page
    if request.method =='POST':
        #get the input
        player = request.POST.get('player_name', '')
        
        #split the input into proper forms
        length = len(player) - 4
        player_name = player[:length]
        acronym = player[length+1:]
        
        #Try to get the player
        try:
            person = Player.objects.filter(name=player_name, team__acronym=acronym)[0]
            
            #Split to the appropriate position page
            if person.pos_code != 'G':
                return redirect(reverse('player_details', kwargs={'id_num': person.id_num}))
            else:
                return redirect(reverse('goalie_details', kwargs={'id_num': person.id_num}))
            
        except:
            #If player does not exist, load the player page
            return redirect(reverse('player_page'))
        
        
  
    #Get the player from the id number and their stats
    person = Player.objects.filter(id_num=id_num)[0]
    details = Stats.objects.filter(player=person)
    
    players = Player.objects.all()
    context = {
        "players": players,
        "player_list": details
        }
    
    template = loader.get_template("players_details.html")
    return HttpResponse(template.render(context, request))

#Get the goalie details page for indiovidual goalies
def goalie_details(request, id_num):
    
    person = Player.objects.filter(id_num=id_num)[0]
    details = GoalieStats.objects.filter(player=person)
    
    players = Player.objects.all()
    context = {
        "players": players,
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
    players, player_list, sort_column, sort_direction, form, fant = process_goalie_request(request)
    
    #Create pages
    paginator = Paginator(player_list, 50)
    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)
    
    #Collect data to send to template
    context = {
        "players": players,
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


def testing(request):
    return HttpResponse("Hello, world!")

