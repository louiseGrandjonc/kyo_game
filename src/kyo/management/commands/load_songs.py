from django.core.management.base import BaseCommand, CommandError

from kyo.models import Artist, Album, Song, Lyrics

from azlyrics.azlyrics import artists, songs, lyrics


class Command(BaseCommand):
    help = 'imports songs band using azlyrics'

    def handle(self, *args, **options):

        azlyrics_dict = {
            'Kyo': 'kyo',
            'Blink182': 'blink182',
            'Maroon5': 'maroon5',
            'Jonas Brothers': 'jonasbrothers',
            'Backstreet Boys': 'bsb',
            'Justin Timberlake': 'timberlake',
            'Smach Mouth': 'smashmouth',
            'Barenaked Ladies': 'barenaked',
            'Korn': 'korn',
            'Avril Lavigne': 'lavigne',
            'Coldplay': 'coldplay',
            'Collective Soul': 'collectivesoul',
            'Bouncing Souls': 'bouncingsouls',
            'Nickelback': 'nickelback'
        }
        for artist_name, azlyrics_name in azlyrics_dict.items():
            artist = Artist.objects.get_or_create(name=artist_name)[0]

            artist_songs = songs(azlyrics_name)

            for album_name, values in artist_songs['albums'].items():
                wait(1)

                album = Album.objects.get_or_create(
                    artist=artist,
                    name=album_name.replace('"', ''),
                    year=values['year'])[0]

                for song_name in values['songs']:
                    song = Song.objects.get_or_create(name=song_name, album=album)[0]

                    if song.lyrics.count():
                        continue

                    azlyrics_lyrics = lyrics(azlyrics_name,
                                             song_name.encode("ascii", errors="ignore").decode())

                    lyrics_obj = Lyrics.objects.create(content=azlyrics_lyrics[0], song=song)
                    wait(3)
