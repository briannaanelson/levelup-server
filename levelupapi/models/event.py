from django.db import models
from levelupapi.models.game import Game


class Event(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    organizer = models.IntegerField()
    
    
    