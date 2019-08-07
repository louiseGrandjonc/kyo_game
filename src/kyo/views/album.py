from django.db.models import Count, Exists, OuterRef, Subquery

from django.views.generic.detail import DetailView


from kyo.models import Album, Song, Lyrics, Word


class AlbumDetailView(DetailView):
    model = Song
    template_name = 'kyo/album/detail.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)


        return context
