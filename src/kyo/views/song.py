from django.db.models import Count, Exists, OuterRef, Subquery

from django.views.generic.detail import DetailView


from kyo.models import Song, Lyrics, Word


class SongDetailView(DetailView):
    model = Song
    template_name = 'kyo/song/detail.html'

    def get_queryset(self):
        return (super().get_queryset()
                .select_related('album')
                .prefetch_related('lyrics', 'words'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['lyrics'] = self.object.lyrics.first()


        # SELECT value, COUNT(*)
        # FROM kyo_word WHERE song_id=342 GROUP BY value ORDER BY 2 DESC LIMIT 10;
        context['top'] = (Word.objects.filter(song=self.object)
                          .values('value')
                          .annotate(total=Count('value'))
                          .order_by('-total')[0:10])


        # words that are unique for this artist
        # How I would write this query

        """

        SELECT id, value, album_id, song_id, artist_id, position FROM kyo_word word  WHERE song_id=342 AND NOT EXISTS (SELECT 1 FROM kyo_word word2  WHERE word2.artist_id=word.artist_id AND word2.value=word.value AND word2.id <> word.id);

        53 ms
        """

        """ Django Query

        SELECT "kyo_word"."id", 
        "kyo_word"."value", 
        "kyo_word"."album_id", 
        "kyo_word"."song_id", 
        "kyo_word"."artist_id", 
        "kyo_word"."position", NOT EXISTS(
        SELECT U0."id", 
               U0."value", 
               U0."album_id", 
               U0."song_id", 
               U0."artist_id", 
               U0."position" 
          FROM "kyo_word" U0 
         WHERE (U0."artist_id" = ("kyo_word"."artist_id") AND U0."value" = ("kyo_word"."value") AND NOT (U0."id" = ("kyo_word"."id")))
        ) AS "is_unique" 
        FROM "kyo_word" 
        WHERE (NOT EXISTS(SELECT U0."id", U0."value", U0."album_id", U0."song_id", U0."artist_id", U0."position" FROM "kyo_word" U0 WHERE (U0."artist_id" = ("kyo_word"."artist_id") AND U0."value" = ("kyo_word"."value") AND NOT (U0."id" = ("kyo_word"."id")))) = true AND "kyo_word"."song_id" = 342)

        53 ms
        """
        same_word_artist = (Word.objects
                            .filter(value=OuterRef('value'),
                                    artist=OuterRef('artist'))
                            .exclude(pk=OuterRef('pk')))

        context['unique_words'] = Word.objects.annotate(is_unique=~Exists(same_word_artist)).filter(is_unique=True, song=self.object)


        # words in chorus or break

        # Group of 2 words that appear the most
        # Using raw
        query = """
        SELECT 1 as id, first_word.value as value, second_word.value as following_word, COUNT(*) as nb_of_occurences
        FROM kyo_word first_word
        INNER JOIN LATERAL (
          SELECT value, position FROM kyo_word next_word
          WHERE next_word.song_id=first_word.song_id
          AND next_word.position > first_word.position
          ORDER BY position ASC LIMIT 1) second_word on true
        WHERE song_id=%s  GROUP BY 1,2,3 HAVING COUNT(*) > %s ORDER BY 4 DESC;"""


        group_of_words = Word.objects.raw(query, [self.object.pk, 1])

        print(group_of_words)

        # Using django ORM (different query)

        next_word_qs = (Word.objects
                        .filter(song_id=self.object.pk,
                                position__gt=OuterRef('position'))
                        .order_by("position")
                        .values('value'))[:1]

        context['words_in_chorus'] = (Word.objects
                                     .annotate(next_word=Subquery(next_word_qs))
                                     .values('value', 'next_word')
                                     .annotate(total=Count('*'))
                                     .filter(song=self.object, total__gt=1)).order_by('-total')


        # words expect the chorus

        words_in_chorus = set([w['value'] for w in context['words_in_chorus']] + [w['next_word'] for w in context['words_in_chorus']])
        context['top_no_chorus'] = (Word.objects.filter(song=self.object)
                                    .exclude(value__in=words_in_chorus)
                                    .values('value')
                                    .annotate(total=Count('value'))
                                    .filter(total__gt=1)
                                    .order_by('-total')[0:10])

        return context
