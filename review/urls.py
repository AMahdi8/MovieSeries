from rest_framework.routers import DefaultRouter

from .views import CommentsViewSet

router = DefaultRouter()
router.register('comment', CommentsViewSet, basename='commnet')

urlpatterns = router.urls
