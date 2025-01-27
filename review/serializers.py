from rest_framework import serializers

from .models import Comment


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'reply', 'movie', 'series', 'username', 'email',
                  'content', 'created_at', 'rating']
        read_only_fields = ['created_at']

    def validate(self, data):
        if not data.get('movie') and not data.get('series'):
            raise serializers.ValidationError(
                "You must specify either movie_id or series_id.")
        if data.get('movie') and data.get('series'):
            raise serializers.ValidationError(
                "You cannot specify both movie_id and series_id.")
        return data
