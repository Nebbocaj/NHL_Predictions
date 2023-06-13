from django.db import models

# Create your models here.
class Team(models.Model):
    name = models.CharField(max_length = 50, default = "")
    division = models.CharField(max_length = 50, default = "")
    conference = models.CharField(max_length = 50, default = "")
    
    played = models.IntegerField(default = 0)
    wins = models.IntegerField(default = 0)
    losses = models.IntegerField(default = 0)
    otl = models.IntegerField(default = 0)
    points = models.IntegerField(default = 0)
    pointPer = models.FloatField(default = 0)
    rw = models.IntegerField(default = 0)
    row = models.IntegerField(default = 0)
    goalsFor = models.IntegerField(default = 0)
    goalsAgainst = models.IntegerField(default = 0)
    goalDiff = models.IntegerField(default = 0)
    
    playoffOdds = models.FloatField(default = 0)
    presidentOdds = models.FloatField(default = 0)
    divisionOdds = models.FloatField(default = 0)
    conferenceOdds = models.FloatField(default = 0)
    div2Odds = models.FloatField(default = 0)
    div3Odds = models.FloatField(default = 0)
    wc1Odds = models.FloatField(default = 0)
    wc2Odds = models.FloatField(default = 0)
    
    def __str__(self):
        return self.name
    

class Odds(models.Model):
    name = models.CharField(max_length = 50, default = "")
    playoff = models.CharField(default = '-1', max_length = 1000)
    
    def get_values(self):
        return list(map(int, self.playoff.split(',')))
    
    def set_values(self, values):
        self.playoff = ','.join(map(str, values))
        
    def __str__(self):
        return self.name