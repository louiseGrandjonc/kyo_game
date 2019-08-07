from django.db import models


from .album import Album
from .lyrics import Word
from .song import Song


class Game(models.Model):
    slug = models.CharField(unique=True, max_length=50)
    album = models.ForeignKey(Album, null=True, on_delete=models.SET_NULL)


class Round(models.Model):
    song = models.ForeignKey(Song, null=True, on_delete=models.SET_NULL)


class Vote(models.Model):
    round = models.ForeignKey(Round, null=True, on_delete=models.SET_NULL)
    game = models.ForeignKey(Game, null=True, on_delete=models.CASCADE)
    player = models.ForeignKey('kyo.Player', on_delete=models.CASCADE)
    word = models.ForeignKey(Word, null=True, on_delete=models.SET_NULL)

    class Meta:
        unique_together = [['game', 'player', 'word']]
