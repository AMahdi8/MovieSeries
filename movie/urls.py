from django.urls import path
from rest_framework.routers import DefaultRouter


from .views import CountryViewSet, GenreViewSet, LanguageViewSet, MovieViewSet, SeriesViewSet

router = DefaultRouter()
router.register('movie', MovieViewSet, basename='movie')
router.register('series', SeriesViewSet, basename='series')
router.register('country', CountryViewSet, basename='country')
router.register('genre', GenreViewSet, basename='genre')
router.register('language', LanguageViewSet, basename='language')


urlpatterns = [
    # path('api/download/<str:token>/',
    #      SecureDownloadView.as_view(), name='secure_download'),
] + router.urls
