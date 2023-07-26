
import numpy as np
from sklearn.linear_model import LinearRegression
from .models import Player, Stats, GoalieStats, CenterAverage, WingAverage, DefAverage, GoalieAverage

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

    for player in Player.objects.all():

        #For all non-goalie players
        if player.pos_code != 'G':

            #Get all seasons for the specified player
            data = list(Stats.objects.filter(player=player))

            #If there is enough data to learn from, use it
            #If not, add dummy data of 0
            if len(data) > 1:
                old_data = data[:-1]
                current_year = data[-1]
            else:
                old_data = data
                current_year = data[0]

            #Loop through all relevent stats to make predictions
            stat_names = ['goals', 'assists', 'blocks', 'shots', 'pim', 'powerPlayPoints', \
                'shortHandPoints', 'hits', 'plusMinus', 'games']
            for stat_name in stat_names:
                #Retrieve data from stats
                y_data = [getattr(season, stat_name) / getattr(season, 'games') for season in old_data]
                x_data = [i for i in range(len(y_data))]
                x_new = [len(y_data)]
                
                #Make the predictions for the current season for each stat
                prediction = make_prediction(x_data, y_data, x_new)[0] * 82.0
                
                #Standardize results
                if stat_name != 'plusMinus':
                    prediction = max(prediction, 0)
                if stat_name == 'games':
                    prediction = min(prediction, 82)

                #Set the prediction to the 2024 season
                setattr(current_year, stat_name, prediction)
                

            #Predict points by adding goals and asissts
            current_year.points = current_year.goals + current_year.assists

            updated_stats.append(current_year)

        elif player.pos_code == 'G':
            #Get all seasons for the specified player
            data = list(GoalieStats.objects.filter(player=player))

            #If there is enough data to learn from, use it
            #If not, add dummy data of 0
            if len(data) > 1:
                old_data = data[:-1]
                current_year = data[-1]
            else:
                old_data = data
                current_year = data[0]

            #Loop through all relevent stats to make predictions
            goalie_stat_names = ['wins', 'losses', 'shutouts', 'saves', 'goalsAgainst', \
            'goalAgainstAverage', 'savePercentage', 'ppSavePercentage', 'shSavePercentage', \
                'evenSavePercentage']
            for stat_name in goalie_stat_names:
                #Retrieve data from stats
                y_data = [getattr(season, stat_name) for season in old_data]
                x_data = [i for i in range(len(y_data))]
                x_new = [len(y_data)]
                
                #Make the predictions for the current season for each stat
                prediction = make_prediction(x_data, y_data, x_new)[0]

                #Standardize results
                prediction = max(prediction, 0.0)
                if stat_name == 'games':
                    prediction = min(prediction, 82.0)
                elif stat_name == 'savePercentage':
                    prediction = round(prediction, 3)
                elif stat_name == 'goalAgainstAverage':
                    prediction = round(prediction, 2)
                elif stat_name in ['ppSavePercentage', 'shSavePercentage', 'evenSavePercentage']:
                    prediction = round(prediction, 1)

                #Set the prediction to the 2024 season
                setattr(current_year, stat_name, prediction)
            
            current_year.games = current_year.wins + current_year.losses

            updated_goalie_stats.append(current_year)


    #Update all data
    Stats.objects.bulk_update(updated_stats, stat_names + ['points'])
    GoalieStats.objects.bulk_update(updated_goalie_stats, goalie_stat_names + ['games'])


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
            'saves': [], 'goalsAgainst': []}
         
                
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


