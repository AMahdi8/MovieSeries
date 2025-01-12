from django.contrib import admin
from django.utils.html import format_html

from .models import *


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'release_year', 'imdb_rating', 'average_rating',
                    'related_countires', 'related_languages', 'related_genres')
    search_fields = ('title',)
    list_filter = ('release_year', 'countries', 'languages', 'genres')
    filter_horizontal = ('countries', 'languages', 'genres')
    autocomplete_fields = ('countries', 'languages', 'genres')

    def related_countires(self, obj):
        countries = obj.countries.all()
        return format_html("<br>".join([country.name for country in countries]))

    def related_languages(self, obj):
        languages = obj.languages.all()
        return format_html("<br>".join([language.name for language in languages]))

    def related_genres(self, obj):
        genres = obj.genres.all()
        return format_html("<br>".join([genre.name for genre in genres]))

    related_countires.short_description = "Countries"
    related_countires.short_description = "Languages"
    related_countires.short_description = "Genres"


@admin.register(Series)
class SeriesAdmin(admin.ModelAdmin):
    list_display = ('title', 'release_year', 'imdb_rating', 'average_rating')
    search_fields = ('title',)
    list_filter = ('release_year',
                   'countries', 'languages', 'genres')
    filter_horizontal = ('countries', 'languages', 'genres')
    autocomplete_fields = ('countries', 'languages', 'genres')


@admin.register(Season)
class SeasonAdmin(admin.ModelAdmin):
    list_display = ('series', 'title', 'number',
                    'release_year', 'avg_duration')
    search_fields = ('series__title', 'title')
    list_filter = ('series', 'release_year')
    autocomplete_fields = ('series', )


@admin.register(Episode)
class EpisodeAdmin(admin.ModelAdmin):
    list_display = ('season', 'title', 'number', 'duration')
    search_fields = ('season__series__title', 'season__title', 'title')
    list_filter = ('season__series', 'season', 'duration')
    autocomplete_fields = ('season', )


@admin.register(DownloadFile)
class DownloadFileAdmin(admin.ModelAdmin):
    list_display = ('movie_or_series', 'quality', 'file')
    search_fields = ('movie__title', 'episode__title', 'quality')
    list_filter = ('quality', 'movie', 'episode')
    autocomplete_fields = ('episode', 'movie')

    def movie_or_series(self, obj):
        return obj.movie.title if obj.movie else obj.episode.season if obj.episode.season else "None"
    movie_or_series.short_description = "Movie/Series"


@admin.register(Subtitle)
class SubtitleAdmin(admin.ModelAdmin):
    list_display = ('language', 'title', 'download_file')
    search_fields = ('language__name', 'title', 'download_file__quality')
    list_filter = ('language',)
    autocomplete_fields = ('download_file', )


@admin.register(Trailer)
class TrailerAdmin(admin.ModelAdmin):
    list_display = ('title', 'movie_or_series', 'upload_date')
    search_fields = ('title', 'movie__title', 'series_season__series__title')
    list_filter = ('upload_date', 'movie', 'series_season')
    autocomplete_fields = ('series_season', 'movie')

    def movie_or_series(self, obj):
        return obj.movie.title if obj.movie else obj.series_season if obj.series_season else "None"
    movie_or_series.short_description = "Movie/Series"
