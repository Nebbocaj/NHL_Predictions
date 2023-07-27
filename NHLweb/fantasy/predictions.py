
import numpy as np
from sklearn.linear_model import LinearRegression
from .models import Player, Stats, GoalieStats, CenterAverage, WingAverage, DefAverage, GoalieAverage
from .players import get_fantasy_goalie_points, get_fantasy_points

#Make predictions on stats based off previous data
def make_prediction(x_train, y_train, x_test):
    # Create a linear regression model
    model = LinearRegression()

    # Reshape x_train and y_train if they are 1D arrays
    x_train = np.array(x_train).reshape(-1, 1)
    y_train = np.array(y_train)

    # Train the model with the given data
    model.fit(x_train, y_train)

    # Reshape x_test if it is a 1D array
    x_test = np.array(x_test).reshape(-1, 1)

    # Make predictions on the test data
    y_pred = model.predict(x_test)

    return y_pred


#Make the predictions for the 2024 season
def predict():

    updated_stats = []
    updated_goalie_stats = []

    CAverage = CenterAverage.objects.all()
    WAverage = WingAverage.objects.all()
    DAverage = DefAverage.objects.all()
    GAverage = GoalieAverage.objects.all()

    #averages = CenterAverage.objects.all()
    #print(getattr(averages[3], 'goals'))

    for player in Player.objects.all():

        #For all non-goalie players
        if player.pos_code != 'G':
            stat_names = ['goals', 'assists', 'blocks', 'shots', 'pim', 'powerPlayPoints', \
                        'shortHandPoints', 'hits', 'plusMinus']
            updated_stats = predict_player(player, updated_stats, stat_names, 0, CAverage, WAverage, DAverage, GAverage)
            

        elif player.pos_code == 'G':
            goalie_stat_names = ['wins', 'losses', 'shutouts', 'saves', 'goalsAgainst', \
             'savePercentage', 'ot']
            updated_goalie_stats = predict_player(player, updated_goalie_stats, goalie_stat_names, 1, CAverage, WAverage, DAverage, GAverage)
            


    #Update all data
    Stats.objects.bulk_update(updated_stats, stat_names + ['points', 'games'])
    GoalieStats.objects.bulk_update(updated_goalie_stats, goalie_stat_names + ['games'])

    player_list = GoalieStats.objects.all()
    get_fantasy_goalie_points(player_list, saveTable = True)

    player_list = Stats.objects.all()
    get_fantasy_points(player_list, saveTable = True)


def predict_player(player, updated_stats, stat_names, state, CAverage, WAverage, DAverage, GAverage):

    year_param = 8

    #Get all seasons for the specified player
    if state == 0:
        data = list(Stats.objects.filter(player=player))
    else:
        data = list(GoalieStats.objects.filter(player=player))


    #If there is enough data to learn from, use it
    #If not, add dummy data of 0
    if len(data) > 1:
        old_data = data[:-1]
        current_year = data[-1]
    else:
        old_data = data
        current_year = data[0]

    veteran = False
    if len(old_data) > year_param:
        old_data = old_data[-year_param:]
        veteran = True

    #Loop through all relevent stats to make predictions
    for stat_name in stat_names:
        #Retrieve data from stats
        if state == 0:
            
            if veteran:
                y_data = [getattr(old_data[y], stat_name) / (getattr(old_data[y], 'games') + 0.00001) for y in range(len(old_data))]

            else:
                if player.pos_code == 'C':
                    y_data = [getattr(old_data[y], stat_name) / (getattr(old_data[y], 'games') + 0.00001) - getattr(CAverage[y], stat_name) for y in range(len(old_data))]
                elif player.pos_code in ['LW', 'RW']:
                    y_data = [getattr(old_data[y], stat_name) / (getattr(old_data[y], 'games') + 0.00001) - getattr(WAverage[y], stat_name) for y in range(len(old_data))]
                elif player.pos_code == 'D':
                    y_data = [getattr(old_data[y], stat_name) / (getattr(old_data[y], 'games') + 0.00001) - getattr(DAverage[y], stat_name) for y in range(len(old_data))]
        else:
            if veteran:
                y_data = [getattr(old_data[y], stat_name) for y in range(len(old_data))]
            else:
                y_data = [getattr(old_data[y], stat_name) - getattr(GAverage[y], stat_name) for y in range(len(old_data))]
        x_data = [i for i in range(len(y_data))]
        x_new = [len(y_data)]
        
        #Make the predictions for the current season for each stat
        if state == 0:
            if veteran:
                prediction = make_prediction(x_data, y_data, x_new)[0] * 82.0
            else:
                prediction = make_prediction(x_data, y_data, x_new)[0] 
                prediction = (prediction + getattr(CAverage[len(old_data)], stat_name)) * 82.0
        else:
            if veteran:
                prediction = make_prediction(x_data, y_data, x_new)[0]
            else:
                prediction = make_prediction(x_data, y_data, x_new)[0] 
                prediction = (prediction + getattr(GAverage[len(old_data)], stat_name))
        #Standardize results
        if state == 0:
            if stat_name != 'plusMinus':
                prediction = max(prediction, 0)
        else:
            prediction = max(prediction, 0.0)
            if stat_name == 'savePercentage':
                prediction = round(prediction, 3)
            elif stat_name == 'goalAgainstAverage':
                prediction = round(prediction, 2)
            elif stat_name in ['ppSavePercentage', 'shSavePercentage', 'evenSavePercentage']:
                prediction = round(prediction, 1)

        #Set the prediction to the 2024 season
        setattr(current_year, stat_name, prediction)
        

    #Further normalize data by adding restrictions
    if state == 0:
        current_year.points = current_year.goals + current_year.assists
        current_year.games = 82
    else:
        total_games = current_year.wins + current_year.losses + current_year.ot
        #Implement a max goalie games of 64
        if  total_games > 64:
            ratio = 64 / total_games
            win_ratio = current_year.wins / total_games
            loss_ratio = current_year.losses / total_games
            current_year.games = 64
            current_year.wins = int(current_year.games * win_ratio)
            current_year.losses = int(current_year.games * loss_ratio)
            current_year.ot = current_year.games - current_year.wins - current_year.losses
            current_year.shutouts = current_year.shutouts * ratio
            current_year.saves = current_year.saves * ratio
            current_year.goalsAgainst = current_year.goalsAgainst * ratio
        current_year.savePercentage = round(current_year.saves / (current_year.saves + current_year.goalsAgainst + 0.00001),3)


    updated_stats.append(current_year)

    return updated_stats


def get_stat_averages():

    #Delete all; entries to start fresh
    center = CenterAverage.objects.all()
    center.delete()
    wing = WingAverage.objects.all()
    wing.delete()
    defence = DefAverage.objects.all()
    defence.delete()
    goalie = GoalieAverage.objects.all()
    goalie.delete()

    #Create empty lists of dictionaryies for the players
    CTotals = [get_empty_totals() for i in range(25)]
    WTotals = [get_empty_totals() for i in range(25)]
    DTotals = [get_empty_totals() for i in range(25)]
    GTotals = [get_empty_goalie_totals() for i in range(25)]

    for player in Player.objects.all():
        
        if player.pos_code != 'G':
            #Get all seasons for the specified player
            data = list(Stats.objects.filter(player=player))[:-1]

            #Append data for each player depending on their position
            if player.pos_code == 'C':
                CTotals = append_player(CTotals, data)
            elif player.pos_code in ['LW', 'RW']:
                WTotals = append_player(WTotals, data)
            elif player.pos_code == 'D':
                DTotals = append_player(DTotals, data)

        #Handle goalie data
        else:
            data = list(GoalieStats.objects.filter(player=player))[:-1]
            GTotals = append_goalie(GTotals, data)
    
    #Collect the average for every year and stat
    CAverage = dict_average(CTotals)
    WAverage = dict_average(WTotals)
    DAverage = dict_average(DTotals)
    GAverage = dict_average(GTotals)

    #Create database entry for centers
    count = 1
    for entry in CAverage:
        entry['year'] = count
        CenterAverage.objects.create(**entry)
        count += 1

    #Create database entry for wingers
    count = 1
    for entry in WAverage:
        entry['year'] = count
        WingAverage.objects.create(**entry)
        count += 1

    #Create database entry for defense
    count = 1
    for entry in DAverage:
        entry['year'] = count
        DefAverage.objects.create(**entry)
        count += 1

    #Create database entry for defense
    count = 1
    for entry in GAverage:
        entry['year'] = count
        GoalieAverage.objects.create(**entry)
        count += 1


#Get an empty dictionary for players
def get_empty_totals():
    return {'goals' : [],'assists' : [],'pim' : [],
            'shots' : [],'games' : [],'hits' : [],
            'blocks' : [],'plusMinus' : [],'points' : [],
            'shifts' : [],'powerPlayPoints' : [],
            'shortHandPoints' : [],'gameWinningGoals' : [],
            'overtimeGoals' : []}


#Get an empty dictionary for goalies
def get_empty_goalie_totals():
    return {'games': [], 'wins': [], 'losses': [], 'shutouts': [], 
            'saves': [], 'goalsAgainst': [], 'savePercentage': [], 'ot': []}
         
                
#Appends all player data into the totals dictionary
def append_player(totals, data):
    count = 0
    for entry in data:
        totals[count]['games'].append(entry.games)
        totals[count]['goals'].append(entry.goals / entry.games) 
        totals[count]['assists'].append(entry.assists / entry.games) 
        totals[count]['points'].append(entry.points / entry.games) 
        totals[count]['plusMinus'].append(entry.plusMinus / entry.games) 
        totals[count]['pim'].append(entry.pim / entry.games) 
        totals[count]['powerPlayPoints'].append(entry.powerPlayPoints / entry.games)  
        totals[count]['shortHandPoints'].append(entry.shortHandPoints / entry.games) 
        totals[count]['shots'].append(entry.shots / entry.games) 
        totals[count]['hits'].append(entry.hits / entry.games) 
        totals[count]['blocks'].append(entry.blocks / entry.games) 
        totals[count]['shifts'].append(entry.shifts / entry.games) 
        totals[count]['gameWinningGoals'].append(entry.gameWinningGoals / entry.games) 
        totals[count]['overtimeGoals'].append(entry.overtimeGoals / entry.games) 
        count += 1

    return totals

#Appends all goalie data into the totals dictionary
def append_goalie(totals, data):
    count = 0
    for entry in data:
        totals[count]['games'].append(entry.games)
        totals[count]['wins'].append(entry.wins / entry.games)
        totals[count]['losses'].append(entry.losses / entry.games)
        totals[count]['shutouts'].append(entry.shutouts / entry.games)
        totals[count]['saves'].append(entry.saves / entry.games)
        totals[count]['goalsAgainst'].append(entry.goalsAgainst / entry.games)
        totals[count]['savePercentage'].append(entry.savePercentage / entry.games)
        totals[count]['ot'].append(entry.ot / entry.games)

        count += 1

    return totals

#Get the average value of each key ina  list of dictionaries
def dict_average(totals):
    averages = [{} for i in range(25)]
    count = 0
    for year in totals:
        for key in year:
            averages[count][key] = round(sum(totals[count][key]) / (len(totals[count][key]) + 0.000000001),3)
        count += 1
    return averages


