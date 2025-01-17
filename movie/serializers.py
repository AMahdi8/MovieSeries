from rest_framework import serializers
from itsdangerous import URLSafeTimedSerializer  # type: ignore
from django.conf import settings

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


# def get_token_serializer():
#     secret_key = settings.SECRET_KEY
#     salt = "secure-download-url"
#     return URLSafeTimedSerializer(secret_key, salt=salt)


# def generate_secure_url(file_id, expires_in=3600):
#     """
#     Generate a secure download URL for the file.
#     Args:
#         file_id (int): The ID of the file.
#         file_path (str): The file's URL or path.
#         expires_in (int): Expiration time in seconds (default: 1 hour).
#     Returns:
#         str: The secure download URL.
#     """
#     serializer = get_token_serializer()
#     token = serializer.dumps({"file_id": file_id})
#     return f"/api/download/{token}?expires_in={expires_in}"


class DownloadFileSerializer(serializers.ModelSerializer):
    # secure_download_url = serializers.SerializerMethodField()

    class Meta:
        model = DownloadFile
        # fields = '__all__'
        fields = ['id', 'file', 'source', 'file_format', 'sticky_subtitles', 'quality',
                  '256-bit-encryption', '10-bit-variant', 'download_url', 'file_size']

    # def get_secure_download_url(self, obj):
    #     serializer = get_token_serializer()
    #     token = serializer.dumps({"file_id": obj.id})
    #     return f"{settings.BASE_URL}/main/api/download/{token}"


class MovieListSerializer(serializers.ModelSerializer):
    director = serializers.SerializerMethodField()
    highest_quality = serializers.SerializerMethodField()
    countries = CountryNameSerializer(many=True)
    languages = LanguageNameSerializer(many=True)
    genres = GenreNameSerializer(many=True)

    class Meta:
        model = Movie
        fields = ['id', 'title', 'release_year', 'countries', 'languages', 'genres', 'highest_quality', 'duration', 'age_category',
                  'imdb_rank', 'imdb_rating', 'image', 'description', 'average_rating', 'director']

    def get_director(self, obj):
        return obj.crews.filter(role='D').values_list('name', flat=True)

    def get_highest_quality(self, obj):
        return f'{obj.highest_source} {obj.highest_quality}'


class MovieDetailSerializer(serializers.ModelSerializer):
    directors = serializers.SerializerMethodField()
    actors = serializers.SerializerMethodField()
    writers = serializers.SerializerMethodField()
    other_stars = serializers.SerializerMethodField()
    highest_quality = serializers.SerializerMethodField()
    countries = CountryNameSerializer(many=True)
    languages = LanguageNameSerializer(many=True)
    genres = GenreNameSerializer(many=True)
    download_urls = DownloadFileSerializer(many=True)

    class Meta:
        model = Movie
        fields = ['id', 'title', 'highest_quality', 'duration', 'countries', 'languages', 'genres', 'directors',
                  'actors', 'writers', 'other_stars', 'age_category', 'description', 'download_urls', 'subtitle_link']

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


class SeriesListSerializer(serializers.ModelSerializer):
    director = serializers.SerializerMethodField()
    countries = CountryNameSerializer(many=True)
    languages = LanguageNameSerializer(many=True)
    genres = GenreNameSerializer(many=True)

    class Meta:
        model = Series
        fields = ['id', 'title', 'release_year', 'end_date', 'age_category', 'description', 'imdb_rank',
                  'imdb_rating', 'image', 'average_rating', 'countries', 'languages', 'genres', 'director']

    def get_director(self, obj):
        return obj.crews.filter(role='D').values_list('name', flat=True)


# generate secure download url
# continue from here
class EpisodeSerializer(serializers.ModelSerializer):
    download_urls = DownloadFileSerializer(many=True)

    class Meta:
        model = Episode
        fields = ['id', 'title', 'number', 'subtitle_link', 'download_urls']


class SeasonSerializer(serializers.ModelSerializer):
    episodes = EpisodeSerializer(many=True)

    class Meta:
        model = Season
        fields = ['id', 'title', 'number', 'avg_duration', 'episodes']


class SeriesDetailSerializer(serializers.ModelSerializer):
    director = serializers.SerializerMethodField()
    actors = serializers.SerializerMethodField()
    writers = serializers.SerializerMethodField()
    other_stars = serializers.SerializerMethodField()
    seasons = SeasonSerializer(many=True)
    countries = CountryNameSerializer(many=True)
    languages = LanguageNameSerializer(many=True)
    genres = GenreNameSerializer(many=True)

    class Meta:
        model = Series
        fields = ['id', 'title', 'release_year', 'end_date', 'age_category', 'description', 'imdb_rank', 'imdb_rating',
                  'average_rating', 'image', 'countries', 'languages', 'genres', 'director', 'actors', 'writers', 'other_stars', 'seasons']

    def get_director(self, obj):
        return obj.crews.filter(role='D').values_list('name', flat=True)

    def get_actors(self, obj):
        return obj.crews.filter(role='A').values_list('name', flat=True)

    def get_writers(self, obj):
        return obj.crews.filter(role='W').values_list('name', flat=True)

    def get_other_stars(self, obj):
        return obj.crews.filter(role='O').values_list('name', flat=True)


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
