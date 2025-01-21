from django.db import models

from movie.models import Movie, Series


class Comment(models.Model):
    movie = models.ForeignKey(
        Movie,
        on_delete=models.CASCADE,
        related_name="comments",
        null=True,
        blank=True
    )
    series = models.ForeignKey(
        Series,
        on_delete=models.CASCADE,
        related_name='comments',
        null=True,
        blank=True
    )
    reply = models.ForeignKey(
        'Comment',
        on_delete=models.CASCADE,
        related_name='comments',
        null=True,
        blank=True
    )
    rating = models.IntegerField(
        choices=[(i, i) for i in range(1, 6)],
        default=1
    )
    username = models.CharField(max_length=255)
    email = models.EmailField()
    content = models.TextField()
    accepted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Comment on {self.movie.title}" if self.movie else f"Comment by on {self.series}"

    def save(self, *args, **kwargs):
        if not self.series and not self.movie:
            raise ValueError(
                "Trailer must be associated with either a movie or a series.")
        if self.series and self.movie:
            raise ValueError(
                "Trailer cannot be associated with both a movie and a series simultaneously.")
        return super().save(*args, **kwargs)
