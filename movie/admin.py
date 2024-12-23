from django.contrib import admin
from django.utils.html import format_html

from .models import *


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('name', )


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', )


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ('name', )


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ['title', 'release_year',
                    'imdb_rank', 'related_countires', 'related_languages', 'related_genres']
    list_editable = ['imdb_rank']

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


admin.site.register(DownloadFile)
admin.site.register(Series)
admin.site.register(Episode)
admin.site.register(Trailer)
admin.site.register(Subtitle)
admin.site.register(Season)
