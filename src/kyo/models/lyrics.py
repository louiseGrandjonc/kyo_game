from django.contrib.postgres.fields import ArrayField
from django.db import models

from .album import Album
from .song import Song


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
    number_of_occurences = models.IntegerField(default=0)
    lyrics = models.ManyToManyField(Lyrics, through='WordLyrics')


class WordLyrics(models.Model):
    lyrics = models.ForeignKey(Lyrics)
    album = models.ForeignKey(Album)
    word = models.ForeignKey(Word)
    position = ArrayField(models.IntegerField(), null=True)
