from django.contrib.postgres.search import SearchVector
from django.core.management.base import BaseCommand, CommandError

from kyo.models import Song, Lyrics, Word, Artist


class Command(BaseCommand):
    help = 'imports songs band using azlyrics'

class Command(BaseCommand):

    def handle(self, *args, **options):

        songs = Song.objects.extra(where=["""
        NOT EXISTS (SELECT 1 FROM "kyo_word" WHERE song_id=kyo_song.id)
        """])

        import ipdb; ipdb.set_trace()
        for song in songs:
            lyrics = song.lyrics.annotate(search=SearchVector('content', config=song.language)).first()
            vectors = lyrics.search.split(' ')
            vector_dict = {}
            for vector in vectors:
                value = vector.split(':')[0].replace("'", '')
                if len(value) < 4:
                    continue
                positions = [int(position) for position in vector.split(':')[1].split(',')]
                vector_dict[value] = positions

            for vector, positions in vector_dict.items():
                for pos in positions:
                    Word.objects.create(value=vector, position=pos, album=song.album, song=song)
