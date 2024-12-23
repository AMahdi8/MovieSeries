from django.db import models


class Country(models.Model):
    name = models.CharField(max_length=60)


class Language(models.Model):
    name = models.CharField(max_length=60)


class Genre(models.Model):
    name = models.CharField(max_length=60)

# class Image(models.Model):
#     image = models.ImageField(upload_to='media/images')


class Actor(models.Model):
    name = models.CharField(max_length=255)
    birth_date = models.DateField()
    bio = models.TextField()
    images = models.ImageField(
        upload_to='media/images/actors/',
        null=True,
        blank=True,
    )
    country = models.ForeignKey(
        Country,
        on_delete=models.DO_NOTHING,
        related_name='actors',
        null=True,
        blank=True
    )


class Movie(models.Model):
    title = models.CharField(max_length=255)
    release_year = models.IntegerField()
    duration = models.IntegerField()
    description = models.TextField()
    imdb_rank = models.IntegerField(default=251)
    imdb_rating = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        null=True,
        blank=True,
    )
    user_rating = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        null=True,
        blank=True,
    )
    image = models.ImageField(
        upload_to='media/images/movie/',
        null=True,
        blank=True
    )
    countries = models.ManyToManyField(
        Country,
        related_name='movies',
    )
    languages = models.ManyToManyField(
        Language,
        related_name='movies',
        blank=True
    )
    genres = models.ManyToManyField(
        Genre,
        related_name='movies',
    )
    actors = models.ManyToManyField(
        Actor,
        related_name='movies'
    )


class Series(models.Model):
    title = models.CharField(max_length=255)
    release_year = models.IntegerField()
    end_date = models.DateField(
        null=True,
        blank=True
    )
    seasons = models.IntegerField(default=1)
    description = models.TextField()
    imdb_rank = models.IntegerField(default=251)
    imdb_rating = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        null=True,
        blank=True,
    )
    user_rating = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        null=True,
        blank=True,
    )
    image = models.ImageField(
        upload_to='media/images/series',
        null=True,
        blank=True
    )
    countries = models.ManyToManyField(
        Country,
        related_name='series',
    )
    languages = models.ManyToManyField(
        Language,
        related_name='series',
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='series',
    )
    actors = models.ManyToManyField(
        Actor,
        related_name='series'
    )


class Episode(models.Model):
    title = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )
    season_number = models.IntegerField()
    episode_number = models.IntegerField()
    duration = models.IntegerField(
        null=True,
        blank=True
    )
    release_date = models.DateField(
        null=True,
        blank=True
    )
    description = models.TextField()
    series = models.ForeignKey(
        Series,
        on_delete=models.CASCADE,
        related_name='episodes'
    )


class Trailer(models.Model):
    title = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )
    url = models.TextField()
    upload_date = models.DateField()
    movie = models.ForeignKey(
        Movie,
        on_delete=models.DO_NOTHING,
        related_name='trailer',
        null=True,
        blank=True
    )
    series = models.ForeignKey(
        Series,
        on_delete=models.DO_NOTHING,
        related_name='trailer',
        null=True,
        blank=True
    )
    season = models.IntegerField(
        null=True,
        blank=True
    )


class DownloadURL(models.Model):
    class QualityChoices(models.TextChoices):
        # Standard Definition
        P144 = '144p', '144p'
        P240 = '240p', '240p'
        P360 = '360p', '360p'
        P480 = '480p', '480p'
        # High Definition
        P720 = '720p', '720p'
        P1080 = '1080p', '1080p'
        # Ultra High Definition
        P1440 = '1440p', '1440p'
        P2160 = '2160p', '2160p'
        P4320 = '4320p', '4320p'
        # 10-bit Variants
        P720_10 = '720p-10bit', '720p-10bit'
        P1080_10 = '1080p-10bit', '1080p-10bit'
        P1440_10 = '1440p-10bit', '1440p-10bit'
        P2160_10 = '2160p-10bit', '2160p-10bit'
        P4320_10 = '4320p-10bit', '4320p-10bit'
        # 256-bit Encryption Variants
        P144_256 = '144p-256', '144p-256'
        P240_256 = '240p-256', '240p-256'
        P360_256 = '360p-256', '360p-256'
        P480_256 = '480p-256', '480p-256'
        P720_256 = '720p-256', '720p-256'
        P1080_256 = '1080p-256', '1080p-256'
        P1440_256 = '1440p-256', '1440p-256'
        P2160_256 = '2160p-256', '2160p-256'
        P4320_256 = '4320p-256', '4320p-256'

    movie = models.ForeignKey(
        Movie,
        on_delete=models.DO_NOTHING,
        related_name='download_urls',
        null=True,
        blank=True
    )
    episode = models.ForeignKey(
        Episode,
        on_delete=models.DO_NOTHING,
        related_name='download_urls',
        null=True,
        blank=True
    )
    file = models.FileField(
        upload_to='media/video/',
        null=True,
        blank=True
    )
    quality = models.CharField(
        max_length=20,
        choices=QualityChoices.choices
    )
    download_url = models.TextField(
        null=True,
        blank=True
    )
