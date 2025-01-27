from django.http import HttpResponseRedirect
from django.db.models import F, Max, Subquery, OuterRef, Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin
from itsdangerous import BadSignature, SignatureExpired  # type: ignore
from django.utils.timezone import now
from datetime import timedelta
from random import sample


from .models import Country, DownloadFile, Genre, Language, Movie, Series
from .serializers import CountrySerializer, GenreSerializer, LanguageSerializer, MovieDetailSerializer, MovieListSerializer, SeriesDetailSerializer, SeriesListSerializer
from .utilities import get_movies_and_series_by_country


class HomePage(APIView):
    def get(self, request):

        choosen_movie = Movie.objects.filter(
            choosen_home_page=True
        )
        choosen_series = Series.objects.filter(
            choosen_home_page=True
        )

        korean_movies, korean_series = get_movies_and_series_by_country(
            'South Korea')
        chinese_movies, chinese_series = get_movies_and_series_by_country(
            'China')
        turkish_movie, turkish_series = get_movies_and_series_by_country(
            'Turkey')

        other_movies = Movie.objects.exclude(
            countries__name__in=["South Korea", "China", "Turkey"]
        ).filter(choosen_country=True)

        other_series = Series.objects.exclude(
            countries__name__in=["South Korea", "China", "Turkey"]
        ).filter(choosen_country=True)

        other_random_movie = sample(
            list(other_movies), min(len(other_movies), 3))
        other_random_series = sample(
            list(other_series), min(len(other_series), 3))

        # Choosen for home page
        choosen_movies_serieslizer = MovieListSerializer(
            choosen_movie, many=True)
        choosen_series_serieslizer = SeriesListSerializer(
            choosen_series, many=True)

        # Korean
        korean_movies_serializer = MovieListSerializer(
            korean_movies, many=True)
        korean_series_serializer = SeriesListSerializer(
            korean_series, many=True)

        # Chinese
        chinese_movies_serializer = MovieListSerializer(
            chinese_movies, many=True)
        chinese_series_serializer = SeriesListSerializer(
            chinese_series, many=True)

        # Turkish
        turkish_movies_serializer = MovieListSerializer(
            turkish_movie, many=True)
        turkish_series_serializer = SeriesListSerializer(
            turkish_series, many=True)

        # foreign countries
        other_movies_serializer = MovieListSerializer(
            other_random_movie, many=True)
        other_series_serializer = SeriesListSerializer(
            other_random_series, many=True)

        return Response({
            "recent_highest_rated": {
                "movies": choosen_movies_serieslizer.data,
                "series": choosen_series_serieslizer.data,
            },
            "korean_content": {
                "movies": korean_movies_serializer.data,
                "series": korean_series_serializer.data,
            },
            "chinese_content": {
                "movies": chinese_movies_serializer.data,
                "series": chinese_series_serializer.data,
            },
            "turkish_content": {
                "movies": turkish_movies_serializer.data,
                "series": turkish_series_serializer.data,
            },
            "other_content": {
                "movies": other_movies_serializer.data,
                "series": other_series_serializer.data,
            },
        })


class SearchView(APIView):
    def get(self, request):
        query = request.query_params.get('q', '').strip()
        if not query:
            return Response({"results": []})

        movies = Movie.objects.filter(title__icontains=query)

        series = Series.objects.filter(title__icontains=query)

        movie_serializer = MovieListSerializer(movies, many=True)
        series_serializer = SeriesListSerializer(series, many=True)

        results = {
            "movies": movie_serializer.data,
            "series": series_serializer.data
        }

        return Response(results)


class MovieViewSet(ListModelMixin,
                   RetrieveModelMixin,
                   GenericViewSet):
    queryset = Movie.objects.prefetch_related(
        'countries', 'languages', 'genres', 'download_urls'
    ).annotate(
        highest_quality=Subquery(
            DownloadFile.objects.filter(movie=OuterRef('pk'))
            .order_by('source', '-quality')
            .values('quality')[:1]
        ),
        highest_source=Subquery(
            DownloadFile.objects.filter(movie=OuterRef('pk'))
            .order_by('source', '-quality')
            .values('source')[:1]
        )
    )

    def get_serializer_class(self):
        if self.action == 'list':
            return MovieListSerializer
        return MovieDetailSerializer


class SeriesViewSet(ListModelMixin,
                    RetrieveModelMixin,
                    GenericViewSet):

    def get_queryset(self):
        if self.action == 'list':
            return Series.objects.prefetch_related(
                'countries', 'languages', 'genres').all()
        return Series.objects.prefetch_related(
            'countries', 'languages', 'genres',
            'seasons', 'seasons__episodes',
            'seasons__episodes__download_urls').all()

    def get_serializer_class(self):
        if self.action == 'list':
            return SeriesListSerializer
        return SeriesDetailSerializer


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
