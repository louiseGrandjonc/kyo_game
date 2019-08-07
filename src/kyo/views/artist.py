from django.db.models import Count, Exists, OuterRef, Subquery, Window, F
from django.db import connection

from django.db.models.functions import DenseRank

from django.views.generic.detail import DetailView

from kyo.models import Song, Lyrics, Word, Artist, Album
from kyo.utils import dictfetchall


class ArtistDetailView(DetailView):
    model = Artist
    template_name = 'kyo/artist/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # number of single words in album
        context['single_word'] = (Word.objects.filter(artist_id=self.object.pk)
                                  .values('album__name')
                                  .annotate(total=Count('id'))
                                  .order_by('-total')[0:10])

        # words that appear in most songs
        # we want the word and in how many song it appears


        """WITH distinct_song AS (SELECT DISTINCT value, song_id FROM kyo_word WHERE artist_id=6)
SELECT value, COUNT(*) FROM distinct_song GROUP BY value ORDER BY count(*) DESC LIMIT 20; """


        # Rank albums by popularity

        dense_rank_by_album = Window(
            expression=DenseRank(),
            order_by=F("popularity").desc()
        )

        context['album_by_popularity'] = (Album.objects
                                          .filter(artist=self.object)
                                          .annotate(ranking=dense_rank_by_album)
                                          .order_by('ranking'))

        # Words with rank on their frequency
        dense_rank_by_album = Window(
            expression=DenseRank(),
            partition_by=F("album_id"),
            order_by=F("frequency").desc()
        )


        context['words'] = (Word.objects
                 .filter(artist_id=self.object)
                 .values('value', 'album_id')
                 .annotate(frequency=Count('value'),
                           ranking=dense_rank_by_album)
                 .order_by('ranking'))

        # top 10 words per album
        # Adding a where on ranking won't work, would need to put it in a subquery
        # So let's do it raw SQL

        query = """
        SELECT value, a.name as album_name, frequency, ranking FROM (

        SELECT value,
        album.name,
        count(*) as frequency,
        dense_rank() OVER (PARTITION BY album.id
        ORDER BY COUNT(*)
        DESC
        ) ranking
        FROM kyo_word INNER JOIN kyo_album album ON album.id = kyo_word.album_id WHERE kyo_word.artist_id = %s   AND value <> 'refrain' GROUP BY value, album.id ORDER BY album.id) a

        WHERE a.ranking < 9 AND a.frequency > 5;"""


        with connection.cursor() as cursor:
            cursor.execute(query, [self.object.pk])
            context['top_10_words'] = dictfetchall(cursor)


        # album with the next
        query = """
        SELECT album.id, album.year, album.popularity,
               next_album.id as next_album_pk,
               next_album.name as next_album_name,
               next_album.year as next_album_year
        FROM kyo_album album
        LEFT OUTER JOIN LATERAL (
          SELECT * FROM kyo_album next_album
          WHERE next_album.artist_id=album.artist_id
        AND next_album.year > album.year
          ORDER BY year ASC LIMIT 1) next_album on true
        WHERE album.artist_id=%s
        ORDER BY album.year;"""


        context['albums'] = Album.objects.raw(query, [self.object.pk])


        # top words total

        context['top_words'] = Word.objects.filter(artist_id=self.object.pk).values('value').annotate(total=Count('id')).order_by('-total')[:30]

        return context
