from rest_framework.routers import DefaultRouter

from .views import CountryViewSet, GenreViewSet, LanguageViewSet, MovieViewSet, SeriesViewSet

router = DefaultRouter()
router.register('movie', MovieViewSet, basename='movie')
router.register('series', SeriesViewSet, basename='series')
router.register('country', CountryViewSet, basename='country')
router.register('genre', GenreViewSet, basename='genre')
router.register('language', LanguageViewSet, basename='language')

urlpatterns = router.urls
