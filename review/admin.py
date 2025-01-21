from django.contrib import admin
from .models import Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'movie_or_series',
                    'rating', 'accepted', 'created_at', 'updated_at')
    list_filter = ('accepted', 'rating', 'created_at', 'updated_at')
    search_fields = ('username', 'email', 'content',
                     'movie__title', 'series__title')
    autocomplete_fields = ('movie', 'series', 'reply')
    actions = ('accept_comments', 'reject_comments')
    list_editable = ('accepted', )

    def movie_or_series(self, obj):
        return obj.movie.title if obj.movie else obj.series.title if obj.series else "None"
    movie_or_series.short_description = "Movie/Series"

    @admin.action(description="Accept selected comments")
    def accept_comments(self, request, queryset):
        queryset.update(accepted=True)

    @admin.action(description="Reject selected comments")
    def reject_comments(self, request, queryset):
        queryset.update(accepted=False)
