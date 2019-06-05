from django.db import models

from .game import Game


class Player(models.Model):
    username = models.CharField(max_length=100, null=False, blank=False)
    game = models.ForeignKey(Game)


