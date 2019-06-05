from django.db import models


from .album import Album
from .lyrics import Word
from .song import Song


class Game(models.Model):
    slug = models.CharField(unique=True, max_length=50)
    album = models.ForeignKey(Album)


class Round(models.Model):
    song = models.ForeignKey(Song)


class Vote(models.Model):
    round = models.ForeignKey(Round)
    game = models.ForeignKey(Game)
    player = models.ForeignKey('kyo.Player')
    word = models.ForeignKey(Word)

    class Meta:
        unique_together = [['game', 'player', 'word']]
