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
        Three_month_ago = now() - timedelta(days=30)

        recent_highest_rated_movies = Movie.objects.filter(
            release_date__gte=Three_month_ago
        ).order_by('rate')[:4]

        recent_highest_rated_series = Series.objects.filter(
            seasons__release_date__gte=Three_month_ago
        ).order_by('rate')[:4]

        korean = get_movies_and_series_by_country('South Korea')
        chinese = get_movies_and_series_by_country('South Korea')
        turkish = get_movies_and_series_by_country('South Korea')

        other_movies = Movie.objects.exclude(
            countries__name__in=["South Korea", "China", "Turkey"]
        ).filter(rate__gte=30)

        other_series = Series.objects.exclude(
            countries__name__in=["South Korea", "China", "Turkey"]
        ).filter(rate__gte=30)

        other_combined = list(other_movies) + list(other_series)

        other_random = sample(other_combined, min(len(other_combined), 3))

        recent_movies_serializer = MovieListSerializer(
            recent_highest_rated_movies, many=True)
        recent_series_serializer = SeriesListSerializer(
            recent_highest_rated_series, many=True)
        korean_serializer = MovieListSerializer(korean, many=True)
        chinese_serializer = MovieListSerializer(chinese, many=True)
        turkish_serializer = MovieListSerializer(turkish, many=True)
        other_serializer = MovieListSerializer(other_random, many=True)
        return Response({
            "recent_highest_rated": {
                "movies": recent_movies_serializer.data,
                "series": recent_series_serializer.data,
            },
            "korean_content": korean_serializer.data,
            "chinese_content": chinese_serializer.data,
            "turkish_content": turkish_serializer.data,
            "other_content": other_serializer.data,
        })


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

#
# class SecureDownloadView(APIView):
#     """
#     View to handle secure file downloads with redirection.
#     """

#     def get(self, request, token):
#         serializer = get_token_serializer()
#         try:
#             # Decode the token and validate expiration
#             data = serializer.loads(token, max_age=int(request.GET.get('expires_in', 3600)))
#         except SignatureExpired:
#             raise PermissionDenied("This link has expired.")
#         except BadSignature:
#             raise PermissionDenied("Invalid download link.")

#         # Retrieve file details from the token
#         file_id = data.get("file_id")
#         file_path = data.get("file_path")

#         # Verify the file exists in the database
#         try:
#             download_file = DownloadFile.objects.get(id=file_id)
#         except DownloadFile.DoesNotExist:
#             raise NotFound("File not found.")

#         # Redirect the user to the file's URL
#         return HttpResponseRedirect(file_path)
