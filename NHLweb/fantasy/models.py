from django.db import models

# Create your models here.
class Player(models.Model):
    
    #Player information
    name = models.CharField(max_length = 50, default = "")
    # team = models.CharField(max_length = 50, default = "")
    # team_id = models.IntegerField(default = 0)
    # number = models.IntegerField(default = 0)
    # age = models.IntegerField(default = 0)
    # height = models.CharField(max_length = 6, default = "")
    # weight = models.IntegerField(default = 0)
    # position = models.CharField(max_length = 5, default = "")
    
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