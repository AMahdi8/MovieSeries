from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import CreateModelMixin
from rest_framework import serializers

from .serializers import CommentSerializer
from .models import Comment


class CommentsViewSet(CreateModelMixin, GenericViewSet):
    queryset = Comment.objects.filter(accepted=True)
    serializer_class = CommentSerializer

    def get_queryset(self):
        """
        فقط کامنت‌های تایید شده را فیلتر کن.
        """
        queryset = super().get_queryset()
        movie_id = self.request.query_params.get('movie_id')
        series_id = self.request.query_params.get('series_id')

        if movie_id:
            queryset = queryset.filter(movie_id=movie_id)
        if series_id:
            queryset = queryset.filter(series_id=series_id)

        return queryset
