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

YEAR_CHOICES = [
    ('all', 'All'),
    ('2006', '2006'),
    ('2007', '2007'),
    ('2008', '2008'),
    ('2009', '2009'),
    ('2010', '2010'),
    ('2011', '2011'),
    ('2012', '2012'),
    ('2013', '2013'),
    ('2014', '2014'),
    ('2015', '2015'),
    ('2016', '2016'),
    ('2017', '2017'),
    ('2018', '2018'),
    ('2019', '2019'),
    ('2020', '2020'),
    ('2021', '2021'),
    ('2022', '2022'),
    ('2023', '2023'),
    ]

#This is the form for  filtering players
class InputForm(forms.Form):
    year = forms.CharField(label='Season:', widget=forms.Select(choices=YEAR_CHOICES), initial='all')
    team = forms.CharField(label='Team:', widget=forms.Select(choices=TEAM_CHOICES), initial='all')
    position = forms.CharField(label='Position:', widget=forms.Select(choices=POSITION_CHOICES), initial='all')
    
#This is the form for customizing fantasy league points
class FantasyScoring(forms.Form):
    goals = forms.IntegerField(label='Goals:', initial=2)
    assist = forms.IntegerField(label='Assists:', initial=1)
    pim = forms.IntegerField(label='PIM:', initial=0)
    shots = forms.IntegerField(label='Shots:', initial=0.1)
    games = forms.IntegerField(label='GP:', initial=0)
    hits = forms.IntegerField(label='Hits:', initial=0.1)
    blocks = forms.IntegerField(label='Blocks:', initial=0.5)
    plusMinus = forms.IntegerField(label='+/-:', initial=0)
    points = forms.IntegerField(label='Points:', initial=0)
    shifts = forms.IntegerField(label='Shifts:', initial=0)
    ppp = forms.IntegerField(label='PPP:', initial=0.5)
    shp = forms.IntegerField(label='SHP:', initial=0.5)
    gwg = forms.IntegerField(label='GWG:', initial=0)
    otg = forms.IntegerField(label='OTG:', initial=0)