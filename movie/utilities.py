from django.db.models import F, Max, Subquery, OuterRef, Q
from random import sample

from .models import *


def get_movies_and_series_by_country(country_name, min_rating=30, max_results=3):
    movies = Movie.objects.filter(
        Q(countries__name=country_name) & Q(rate__gte=min_rating)
    )
    series = Series.objects.filter(
        Q(countries__name=country_name) & Q(rate__gte=min_rating)
    )

    combined = list(movies) + list(series)
    random_selection = sample(combined, min(len(combined), max_results))

    return random_selection
