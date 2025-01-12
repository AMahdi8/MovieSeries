from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin

from movie.models import Country, Genre, Language, Movie, Series
from movie.serializers import CountrySerializer, GenreSerializer, LanguageSerializer, MovieSerializer, SeriesSerializer


class MovieViewSet(ListModelMixin,
                   RetrieveModelMixin,
                   GenericViewSet):
    queryset = Movie.objects.prefetch_related(
        'countries', 'languages', 'genres').all()
    serializer_class = MovieSerializer


class SeriesViewSet(ListModelMixin,
                    RetrieveModelMixin,
                    GenericViewSet):
    queryset = Series.objects.prefetch_related(
        'countries', 'languages', 'genres').all()
    serializer_class = SeriesSerializer


class CountryViewSet(RetrieveModelMixin,
                     GenericViewSet):
    queryset = Country.objects.prefetch_related(
        'series', 'movies').all()
    serializer_class = CountrySerializer
    lookup_field = 'name'


class LanguageViewSet(RetrieveModelMixin,
                      GenericViewSet):
    queryset = Language.objects.prefetch_related(
        'series', 'movies').all()
    serializer_class = LanguageSerializer
    lookup_field = 'name'


class GenreViewSet(RetrieveModelMixin,
                   GenericViewSet):
    queryset = Genre.objects.prefetch_related(
        'series', 'movies').all()
    serializer_class = GenreSerializer
    lookup_field = 'name'
