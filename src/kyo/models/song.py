from django.db import models

from .album import Album


class Song(models.Model):
    name = models.CharField(max_length=255, null=False)
    album = models.ForeignKey(Album, related_name='songs', on_delete=models.CASCADE)
    language = models.CharField(max_length=255, default='english')

    class Meta:
        unique_together = [['name', 'album']]


    def __str__(self):
        return self.name
