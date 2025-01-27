from django.db.models import F, Max, Subquery, OuterRef, Q
from random import sample

from .models import *


def get_movies_and_series_by_country(country_name, max_results=3):
    movies = Movie.objects.filter(
        Q(countries__name=country_name) & Q(choosen_country=True)
    )
    series = Series.objects.filter(
        Q(countries__name=country_name) & Q(choosen_country=True)
    )

    random_movies = sample(list(movies), min(len(movies), max_results))
    random_series = sample(list(series), min(len(series), max_results))

    return [random_movies, random_series]
