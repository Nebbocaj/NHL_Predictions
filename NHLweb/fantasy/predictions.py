
import numpy as np
from sklearn.linear_model import LinearRegression
from .models import Player, Stats, GoalieStats

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
        print(player.name, player.id_num)

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
                y_data = [getattr(season, stat_name) for season in old_data]
                x_data = [i for i in range(len(y_data))]
                x_new = [len(y_data)]
                
                #Make the predictions for the current season for each stat
                prediction = make_prediction(x_data, y_data, x_new)[0]
                
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
            goalie_stat_names = ['wins', 'games', 'losses', 'shutouts', 'saves', 'goalsAgainst', \
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
            

            updated_goalie_stats.append(current_year)


    #Update all data
    Stats.objects.bulk_update(updated_stats, stat_names + ['points'])
    GoalieStats.objects.bulk_update(updated_goalie_stats, goalie_stat_names)



