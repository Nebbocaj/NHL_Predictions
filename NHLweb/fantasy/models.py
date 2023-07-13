from django.db import models


class Team(models.Model):
    name = models.CharField(max_length = 50, default = "")
    division = models.CharField(max_length = 50, default = "")
    conference = models.CharField(max_length = 50, default = "")
    acronym = models.CharField(max_length = 3, default = "") #3 letter abreviation
    id_num = models.IntegerField(default = -1) #Id number for NHL api
    
    def __str__(self):
        return self.name

# Create your models here.
class Player(models.Model):
    
    #Player information
    name = models.CharField(max_length = 50, default = "")
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    
    number = models.IntegerField(default = -1)
    age = models.IntegerField(default = -1)
    height = models.CharField(max_length = 3, default = "X") #In foot, inches
    weight = models.IntegerField(default = -1) #in pounds
    id_num = models.IntegerField(default = -1) #Id num for NHL api
    country = models.CharField(max_length = 20, default = "N/A")
    position = models.CharField(max_length = 20, default = "N/A")
    pos_code = models.CharField(max_length = 3, default = "X")
    
    def __str__(self):
        return self.name
    
class Season(models.Model):
    year = models.IntegerField()
    current_season = models.BooleanField(default = False) #marks which season is the current season
    
    def __str__(self):
        return str(self.year)
    
    
class Stats(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    season = models.ForeignKey(Season, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True)
    
    goals = models.IntegerField(default = 0)
    assists = models.IntegerField(default = 0)
    toi = models.CharField(max_length = 12, default = "N/A")
    pim = models.IntegerField(default = 0)
    shots = models.IntegerField(default = 0)
    games = models.IntegerField(default = 0)
    hits = models.IntegerField(default = 0)
    blocks = models.IntegerField(default = 0)
    plusMinus = models.IntegerField(default = 0)
    points = models.IntegerField(default = 0)
    shifts = models.IntegerField(default = 0)
    
    faceoffPct = models.FloatField(default = 0)
    shotPct = models.FloatField(default = 0)
    
    powerPlayGoals = models.IntegerField(default = 0)
    powerPlayPoints = models.IntegerField(default = 0)
    powerPlayTOI = models.CharField(max_length = 12, default = "N/A")
    shortHandGoals = models.IntegerField(default = 0)
    shortHandPoints = models.IntegerField(default = 0)
    shortHandTOI = models.CharField(max_length = 12, default = "N/A")
    
    gameWinningGoals = models.IntegerField(default = 0)
    overtimeGoals = models.IntegerField(default = 0)
    
    evenTOI = models.CharField(max_length = 12, default = "N/A")
    
    fantasyPoints = models.FloatField(default = 0)
    

    def __str__(self):
        return f"{self.player.name} - {self.season.year}"
    
class GoalieStats(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    season = models.ForeignKey(Season, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True)
    
    games = models.IntegerField(default = 0)
    wins = models.IntegerField(default = 0)
    losses = models.IntegerField(default = 0)
    ot = models.IntegerField(default = 0)
    shutouts = models.IntegerField(default = 0)
    saves = models.IntegerField(default = 0)
    
    powerPlaySaves = models.IntegerField(default = 0)
    shortHandSaves = models.IntegerField(default = 0)
    evenSaves = models.IntegerField(default = 0)
    powerPlayShots = models.IntegerField(default = 0)
    shortHandShots = models.IntegerField(default = 0)
    evenShots = models.IntegerField(default = 0)
    
    savePercentage = models.FloatField(default = 0)
    goalAgainstAverage = models.FloatField(default = 0)
    ppSavePercentage = models.FloatField(default = 0)
    shSavePercentage = models.FloatField(default = 0)
    evenSavePercentage = models.FloatField(default = 0)
    
    shotsAgainst = models.IntegerField(default = 0)
    goalsAgainst = models.IntegerField(default = 0)
    
    toi = models.CharField(max_length = 12, default = "N/A")
    
    fantasyPoints = models.FloatField(default = 0)
