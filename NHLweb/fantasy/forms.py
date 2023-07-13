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
    
#This is the form for  filtering goalies
class GoalieInputForm(forms.Form):
    year = forms.CharField(label='Season:', widget=forms.Select(choices=YEAR_CHOICES), initial='all')
    team = forms.CharField(label='Team:', widget=forms.Select(choices=TEAM_CHOICES), initial='all')
    
#This is the form for customizing fantasy league points
class FantasyScoring(forms.Form):
    games = forms.IntegerField(label='GP:', initial=0, widget=forms.NumberInput(attrs={'class': 'small-input'}))
    goals = forms.IntegerField(label='G:', initial=2, widget=forms.NumberInput(attrs={'class': 'small-input'}))
    assist = forms.IntegerField(label='A:', initial=1, widget=forms.NumberInput(attrs={'class': 'small-input'}))
    points = forms.IntegerField(label='P:', initial=0, widget=forms.NumberInput(attrs={'class': 'small-input'}))
    plusMinus = forms.IntegerField(label='+/-:', initial=0, widget=forms.NumberInput(attrs={'class': 'small-input'}))
    pim = forms.IntegerField(label='PIM:', initial=0, widget=forms.NumberInput(attrs={'class': 'small-input'}))
    ppp = forms.IntegerField(label='PPP:', initial=0.5, widget=forms.NumberInput(attrs={'class': 'small-input'}))
    shp = forms.IntegerField(label='SHP:', initial=0.5, widget=forms.NumberInput(attrs={'class': 'small-input'}))
    shots = forms.IntegerField(label='SOG:', initial=0.1, widget=forms.NumberInput(attrs={'class': 'small-input'}))
    hits = forms.IntegerField(label='HIT:', initial=0.1, widget=forms.NumberInput(attrs={'class': 'small-input'}))
    blocks = forms.IntegerField(label='BLK:', initial=0.5, widget=forms.NumberInput(attrs={'class': 'small-input'}))
    
    shifts = forms.IntegerField(label='Shifts:', initial=0, widget=forms.NumberInput(attrs={'class': 'small-input'}))
    gwg = forms.IntegerField(label='GWG:', initial=0, widget=forms.NumberInput(attrs={'class': 'small-input'}))
    otg = forms.IntegerField(label='OTG:', initial=0, widget=forms.NumberInput(attrs={'class': 'small-input'}))
    
#This is the form for customizing fantasy league points for goalies
class GoalieFantasyScoring(forms.Form):
    games = forms.IntegerField(label='GP:', initial=0, widget=forms.NumberInput(attrs={'class': 'small-input'}))
    wins = forms.IntegerField(label='W:', initial=4, widget=forms.NumberInput(attrs={'class': 'small-input'}))
    losses = forms.IntegerField(label='L:', initial=0, widget=forms.NumberInput(attrs={'class': 'small-input'}))
    shutouts = forms.IntegerField(label='SO:', initial=3, widget=forms.NumberInput(attrs={'class': 'small-input'}))
    saves = forms.IntegerField(label='Saves:', initial=0.2, widget=forms.NumberInput(attrs={'class': 'small-input'}))
    goalsAgainst = forms.IntegerField(label='GA:', initial=-2, widget=forms.NumberInput(attrs={'class': 'small-input'}))