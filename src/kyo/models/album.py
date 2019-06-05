from django.db import models

from .artist import Artist


class Album(models.Model):
    name = models.CharField(max_length=255, null=False)
    year = models.IntegerField()
    artist = models.ForeignKey(Artist)

    class Meta:
        unique_together = [['name', 'artist']]
