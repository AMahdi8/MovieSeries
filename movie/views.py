from django.http import HttpResponseRedirect
from django.db.models import F, Max, Subquery, OuterRef
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin
from itsdangerous import BadSignature, SignatureExpired  # type: ignore

from .models import Country, DownloadFile, Genre, Language, Movie, Series
from .serializers import CountrySerializer, GenreSerializer, LanguageSerializer, MovieDetailSerializer, MovieListSerializer, SeriesDetailSerializer, SeriesListSerializer


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
