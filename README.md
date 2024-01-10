# NHL_Predictions

This is a work-in-progress website for making various predictions for the National Hockey League (NHL). The goal is to include odds about which teams will make the playoffs at any given point in the season, which players will win individial awards, create power rankings for players and teams, and create informative graphics for all information presented.

## Plan

### Player Fantasy Point Prediction
This is the current main goal of the project. At the beginning of the NHL season, the goal of this part is to provide a model that can give estimates for goals, assists, hits, blocks, etc. for each player. It will then take all of these projected points and give an "expected fantasy points" score for each player based on a user's specific fantasy league rules. It will use data analytics to make individual predictions on each stat.

### Team Playoff Prediction
The current functionality here is to provide a couple of basic tables that show the current team stats for all teams as well as the probability of a team making playoffs or winning specific titles. A lot of the functionality is already in place. Two main things need to be done here. 1: add an ELO system to better model team statistics. 2: add Django channels so that the website will automatically update with new data in the morning after games. 



