import random

import time

from django.core.management.base import BaseCommand, CommandError

from kyo.models import Artist, Album, Song, Lyrics

from azlyrics.azlyrics import artists, songs, lyrics


class Command(BaseCommand):
    help = 'imports songs band using azlyrics'

    def handle(self, *args, **options):

        azlyrics_dict = {
            # 'Blink-182': 'blink'
            # 'Maroon5': 'maroon5'
            # 'Jonas Brothers': 'jonasbrothers',
            # 'Justin Timberlake': 'timberlake',
            # 'Avril Lavigne': 'lavigne',

            'Backstreet Boys': 'bsb',
            # 'Smach Mouth': 'smashmouth',
            # 'Barenaked Ladies': 'barenaked',
            # 'Korn': 'korn',
            # 'Coldplay': 'coldplay',
            # 'Collective Soul': 'collectivesoul',
            # 'Bouncing Souls': 'bouncingsouls',
            # 'Nickelback': 'nickelback'
        }
        nb_calls = 0
        for artist_name, azlyrics_name in azlyrics_dict.items():
            artist = Artist.objects.get_or_create(name=artist_name)[0]


            try:
                artist_songs = songs(azlyrics_name)
            except:
                import ipdb; ipdb.set_trace()
                break

            nb_calls += 1

            for album_name, values in artist_songs['albums'].items():
                time.sleep(random.uniform(3, 6))

                album = Album.objects.get_or_create(
                    artist=artist,
                    name=album_name.replace('"', ''),
                    year=values['year'])[0]

                for song_name in values['songs']:

                    if nb_calls > 50:
                        return

                    song = Song.objects.get_or_create(name=song_name, album=album)[0]

                    if song.lyrics.count():
                        continue

                    if azlyrics_name == 'blink':
                        azlyrics_name = 'blink182'

                    if azlyrics_name == 'timberlake':
                        azlyrics_name = 'justintimberlake'

                    if azlyrics_name == 'lavigne':
                        azlyrics_name = 'avrillavigne'

                    if azlyrics_name  == 'bsb':
                        azlyrics_name = 'backstreetboys'


                    azlyrics_lyrics = lyrics(azlyrics_name,
                                             song_name.encode("ascii", errors="ignore").decode())


                    try:
                        lyrics_obj = Lyrics.objects.create(content=azlyrics_lyrics[0], song=song)
                    except:
                        import ipdb; ipdb.set_trace()
                    nb_calls += 1
                    time.sleep(random.uniform(3, 6))
