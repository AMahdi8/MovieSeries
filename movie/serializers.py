from rest_framework import serializers
from itsdangerous import URLSafeTimedSerializer  # type: ignore
from django.conf import settings

from review.serializers import CommentSerializer

from .models import Country, DownloadFile, Episode, Genre, Language, Movie, Season, Series


class CountryNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['name']


class GenreNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['name']


class LanguageNameSerializer(serializers.ModelSerializer):

    class Meta:
        model = Language
        fields = ['name']


class DownloadFileSerializer(serializers.ModelSerializer):

    class Meta:
        model = DownloadFile
        fields = ['id', 'source', 'file_format', 'sticky_subtitles', 'quality',
                  '256-bit-encryption', '10-bit-variant', 'download_url', 'file_size']


class MovieListSerializer(serializers.ModelSerializer):
    director = serializers.SerializerMethodField()
    highest_quality = serializers.SerializerMethodField()
    countries = CountryNameSerializer(many=True)
    languages = LanguageNameSerializer(many=True)
    genres = GenreNameSerializer(many=True)

    class Meta:
        model = Movie
        fields = ['id', 'title', 'release_year', 'countries', 'languages', 'genres', 'highest_quality', 'duration', 'age_category',
                  'imdb_rank', 'rate', 'image', 'description', 'average_rating', 'director']

    def get_director(self, obj):
        return obj.crews.filter(role='D').values_list('name', flat=True)

    def get_highest_quality(self, obj):
        highest_source = getattr(obj, 'highest_source', None)
        highest_quality = getattr(obj, 'highest_quality', None)
        if not highest_quality and not highest_source:
            return None
        return f'{highest_source} {highest_quality}'


class MovieDetailSerializer(serializers.ModelSerializer):
    directors = serializers.SerializerMethodField()
    actors = serializers.SerializerMethodField()
    writers = serializers.SerializerMethodField()
    other_stars = serializers.SerializerMethodField()
    highest_quality = serializers.SerializerMethodField()
    # trailers_urls = serializers.SerializerMethodField()
    accepted_comments = serializers.SerializerMethodField()
    related_movies = serializers.SerializerMethodField()
    countries = CountryNameSerializer(many=True)
    languages = LanguageNameSerializer(many=True)
    genres = GenreNameSerializer(many=True)
    download_urls = DownloadFileSerializer(many=True)

    class Meta:
        model = Movie
        fields = ['id', 'title', 'highest_quality', 'duration', 'imdb_rank', 'rate',
                  'countries', 'languages', 'genres', 'directors', 'actors', 'writers',
                  'other_stars', 'age_category', 'description', 'subtitle_link',
                  'trailer_link', 'download_urls', 'related_movies', 'accepted_comments']

    def get_highest_quality(self, obj):
        return f'{obj.highest_source} {obj.highest_quality}'

    def get_directors(self, obj):
        return obj.crews.filter(role='D').values_list('name', flat=True)

    def get_actors(self, obj):
        return obj.crews.filter(role='A').values_list('name', flat=True)

    def get_writers(self, obj):
        return obj.crews.filter(role='W').values_list('name', flat=True)

    def get_other_stars(self, obj):
        return obj.crews.filter(role='O').values_list('name', flat=True)

    # def get_trailers_urls(self, obj):
    #     return obj.trailers.values_list('url', flat=True)

    def get_accepted_comments(self, obj):
        accepted_comments = obj.comments.filter(accepted=True)
        return CommentSerializer(accepted_comments, many=True).data

    def get_related_movies(self, obj):
        related_movies = Movie.objects.filter(
            genres__in=obj.genres.all()
        ).exclude(id=obj.id)

        related_movies = related_movies.order_by('?')[:6]
        return MovieListSerializer(related_movies, many=True).data


class SeriesListSerializer(serializers.ModelSerializer):
    director = serializers.SerializerMethodField()
    countries = CountryNameSerializer(many=True)
    languages = LanguageNameSerializer(many=True)
    genres = GenreNameSerializer(many=True)

    class Meta:
        model = Series
        fields = ['id', 'title', 'release_year', 'end_date', 'age_category', 'description', 'imdb_rank',
                  'rate', 'image', 'average_rating', 'countries', 'languages', 'genres', 'director']

    def get_director(self, obj):
        return obj.crews.filter(role='D').values_list('name', flat=True)


class EpisodeSerializer(serializers.ModelSerializer):
    download_urls = DownloadFileSerializer(many=True)

    class Meta:
        model = Episode
        fields = ['id', 'title', 'number', 'subtitle_link', 'download_urls']


class SeasonSerializer(serializers.ModelSerializer):
    # trailers_urls = serializers.SerializerMethodField()
    episodes = EpisodeSerializer(many=True)

    class Meta:
        model = Season
        fields = ['id', 'title', 'number', 'avg_duration',
                  'is_finished', 'description', 'trailer_link', 'episodes']

    # def get_trailers_urls(self, obj):
    #     return obj.trailers.values_list('url', flat=True)


class SeriesDetailSerializer(serializers.ModelSerializer):
    director = serializers.SerializerMethodField()
    actors = serializers.SerializerMethodField()
    writers = serializers.SerializerMethodField()
    other_stars = serializers.SerializerMethodField()
    accepted_comments = serializers.SerializerMethodField()
    related_series = serializers.SerializerMethodField()
    seasons = SeasonSerializer(many=True)
    countries = CountryNameSerializer(many=True)
    languages = LanguageNameSerializer(many=True)
    genres = GenreNameSerializer(many=True)

    class Meta:
        model = Series
        fields = ['id', 'title', 'release_year', 'end_date', 'age_category', 'description', 'imdb_rank', 'rate',
                  'average_rating', 'image', 'countries', 'languages', 'genres', 'director', 'actors', 'writers', 'other_stars', 'seasons', 'related_series', 'accepted_comments']

    def get_director(self, obj):
        return obj.crews.filter(role='D').values_list('name', flat=True)

    def get_actors(self, obj):
        return obj.crews.filter(role='A').values_list('name', flat=True)

    def get_writers(self, obj):
        return obj.crews.filter(role='W').values_list('name', flat=True)

    def get_other_stars(self, obj):
        return obj.crews.filter(role='O').values_list('name', flat=True)

    def get_accepted_comments(self, obj):
        accepted_comments = obj.comments.filter(accepted=True)
        return CommentSerializer(accepted_comments, many=True).data

    def get_related_series(self, obj):
        related_series = Series.objects.filter(
            genres__in=obj.genres.all()
        ).exclude(id=obj.id)

        related_series = related_series.order_by('?')[:6]
        return SeriesListSerializer(related_series, many=True).data


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['name', 'movies', 'series']

    movies = MovieListSerializer(many=True)
    series = SeriesListSerializer(many=True)


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['name', 'movies', 'series']

    movies = MovieListSerializer(many=True)
    series = SeriesListSerializer(many=True)


class LanguageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Language
        fields = ['name', 'movies', 'series']

    movies = MovieListSerializer(many=True)
    series = SeriesListSerializer(many=True)
