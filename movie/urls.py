from django.urls import path
from rest_framework.routers import DefaultRouter


from .views import CountryViewSet, GenreViewSet, HomePage, LanguageViewSet, MovieViewSet, SearchView, SeriesViewSet

router = DefaultRouter()
router.register('movie', MovieViewSet, basename='movie')
router.register('series', SeriesViewSet, basename='series')
router.register('country', CountryViewSet, basename='country')
router.register('genre', GenreViewSet, basename='genre')
router.register('language', LanguageViewSet, basename='language')


urlpatterns = [
    path('search/', SearchView.as_view(), name='search'),
] + router.urls
