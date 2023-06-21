# NHL_Predictions

This is a website for making various predictions for the National Hockey League (NHL). The goal is to include odds about which teams will make the playoffs at any given point in the season, which players will win individial awards, create power rankings for players and teams, and create informative graphics for all information presented.

## Plan

### Team Playoff Prediction
Each day during the regular season of the 2023/2024 season, the site will query the current standings for the NHL and store it in the website database. It will then convert that data into a temporary dataframe, run lots (10,000?) of season simulations, and provide odds for making the playoffs, winning the division, etc. Each of these odds will then be put back into the website database to display on the standings page. Each of the odds will also be stores in a separate table of historical playoff odds so that it can be displayed via a graph on a playoff prediction page.

For now, there are some functions that allow standings to be calculated at a specific point of an NHL season. The functions are get_game_status, initialize_dataframe, calculate standings, and get_old_standings. They are for testing out odds from aspecific point as more features are developed over the summer. They also may be used later as a sort of playoff odds "time machine" on a separate page of the website.

### Player Fantasy Point Prediction
At the beginning of the NHL season, the goal of this part is to provide a model which can give estimates for goals, assists, hits, blocks, etc. for each player. It will then take all of these projected points and give an "expected fantasy points" score for each player based of a user's specific fantasy league rules. 


