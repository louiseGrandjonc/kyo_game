from django.contrib.postgres.fields import ArrayField
from django.db import models

from .album import Album
from .song import Song
from .artist import Artist


class Lyrics(models.Model):
    VERSE = 0
    CHORUS = 1
    BREAK = 2
    TYPE_CHOICES = (
        (CHORUS, 'Chorus'),
        (VERSE, 'Verse'),
        (BREAK, 'Break')
    )
    type = models.IntegerField(choices=TYPE_CHOICES,
                               default=VERSE)
    content = models.TextField()
    song = models.ForeignKey(Song, on_delete=models.CASCADE,
                             related_name='lyrics')
    position = models.IntegerField(default=0)


class Word(models.Model):
    value = models.CharField(max_length=255)
    album = models.ForeignKey(Album, null=True, on_delete=models.CASCADE)
    song = models.ForeignKey(Song, null=True, related_name='words', on_delete=models.CASCADE)
    artist = models.ForeignKey(Artist, null=True, related_name='words', on_delete=models.CASCADE)
    position = models.IntegerField(default=0)

    def __str__(self):
        return '%s: %s: %d' % (self.song.name, self.value, self.position)
