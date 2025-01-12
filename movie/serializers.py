from rest_framework import serializers

from .models import Country, DownloadFile, Episode, Genre, Language, Movie, Season, Series


class DownloadFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = DownloadFile
        fields = '__all__'


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['title', 'download_urls']

    download_urls = DownloadFileSerializer(many=True)


class EpisodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Episode
        fields = ['title', 'number', 'download_urls']

    download_urls = DownloadFileSerializer(many=True)


class SeasonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Season
        fields = ['number', 'episodes']

    episodes = EpisodeSerializer(many=True)


class SeriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Series
        fields = ['title', 'seasons']

    seasons = SeasonSerializer(many=True)


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['name', 'movies', 'series']

    movies = MovieSerializer(many=True)
    series = SeriesSerializer(many=True)


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['name', 'movies', 'series']

    movies = MovieSerializer(many=True)
    series = SeriesSerializer(many=True)


class LanguageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Language
        fields = ['name', 'movies', 'series']

    movies = MovieSerializer(many=True)
    series = SeriesSerializer(many=True)
