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
    
    def __str__(self):
        return self.name
    

class Odds(models.Model):
    team = models.CharField(default = '', max_length = 1000)
    
    def get_values(self):
        return list(map(int, self.values.split(',')))
    
    def set_values(self, values):
        self.values = ','.join(map(str, values))
        
    def __str__(self):
        return f"IntegerArray: {self.get_values()}"