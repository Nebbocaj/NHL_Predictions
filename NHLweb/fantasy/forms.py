from django import forms

POSITION_CHOICES = [
    ('all', 'All'),
    ('C','Center'),
    ('RW', 'Right Wing'),
    ('LW', 'Left Wing'),
    ('D', 'Defense')
    ]

TEAM_CHOICES = [
    ('all', 'All'),
    ('ANA', 'Anaheim Ducks'),
    ('ARI', 'Arizona Coyotes'),
    ('BOS', 'Boston Bruins'),
    ('BUF', 'Buffalo Sabres'),
    ('CGY', 'Calgary Flames'),
    ('CAR', 'Carolina Hurricanes'),
    ('CHI', 'Chicago Blackhawks'),
    ('COL', 'Colorado Avalanche'),
    ('CBJ', 'Columbus Blue Jackets'),
    ('DAL', 'Dallas Stars'),
    ('DET', 'Detroit Red Wings'),
    ('EDM', 'Edmonton Oilers'),
    ('FLA', 'Florida Panthers'),
    ('LAK', 'Los Angeles Kings'),
    ('MIN', 'Minnesota Wild'),
    ('MTL', 'Montréal Canadiens'),
    ('NSH', 'Nashville Predators'),
    ('NJD', 'New Jersey Devils'),
    ('NYI', 'New York Islanders'),
    ('NYR', 'New York Rangers'),
    ('OTT', 'Ottawa Senators'),
    ('PHI', 'Philadelphia Flyers'),
    ('PIT', 'Pittsburgh Penguins'),
    ('SJS', 'San Jose Sharks'),
    ('SEA', 'Seattle Kraken'),
    ('STL', 'St. Louis Blues'),
    ('TBL', 'Tampa Bay Lightning'),
    ('TOR', 'Toronto Maple Leafs'),
    ('VAN', 'Vancouver Canucks'),
    ('VGK', 'Vegas Golden Knights'),
    ('WSH', 'Washington Capitals'),
    ('WPG', 'Winnipeg Jets')
    ]

class InputForm(forms.Form):
    team = forms.CharField(label='Team:', widget=forms.Select(choices=TEAM_CHOICES), initial='all')
    position = forms.CharField(label='Position:', widget=forms.Select(choices=POSITION_CHOICES), initial='all')