from django.db import models

# Create your models here.
class Team(models.Model):
    name = models.CharField(max_length = 50)
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