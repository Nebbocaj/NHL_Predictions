from django.db import models


class Team(models.Model):
    name = models.CharField(max_length = 50, default = "")
    division = models.CharField(max_length = 50, default = "")
    conference = models.CharField(max_length = 50, default = "")
    acronym = models.CharField(max_length = 3, default = "")
    id_num = models.IntegerField(default = -1) #Id number for NHL api
    
    def __str__(self):
        return self.name

# Create your models here.
class Player(models.Model):
    
    #Player information
    name = models.CharField(max_length = 50, default = "")
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    
    #Stats for year
    
    def __str__(self):
        return self.name
    
class Season(models.Model):
    year = models.IntegerField()
    
    def __str__(self):
        return str(self.year)
    
    
class Stats(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    season = models.ForeignKey(Season, on_delete=models.CASCADE)
    goals = models.IntegerField(default = 0)
    assists = models.IntegerField(default = 0)

    def __str__(self):
        return f"{self.player.name} - {self.season.year}"
    
