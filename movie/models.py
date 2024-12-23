from django.db import models


class Country(models.Model):
    name = models.CharField(max_length=60, unique=True)

    def __str__(self):
        return self.name


class Language(models.Model):
    name = models.CharField(max_length=60, unique=True)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=60, unique=True)

    def __str__(self):
        return self.name

# Actor could be add later i dont need it right now
# class Actor(models.Model):
#     name = models.CharField(max_length=255)
#     birth_date = models.DateField()
#     bio = models.TextField()
#     images = models.ImageField(
#         upload_to='media/images/actors/',
#         null=True,
#         blank=True,
#     )
#     country = models.ForeignKey(
#         Country,
#         on_delete=models.DO_NOTHING,
#         related_name='actors',
#         null=True,
#         blank=True
#     )

#     def __str__(self):
#         return self.name


class Movie(models.Model):
    title = models.CharField(max_length=255)
    release_year = models.IntegerField()
    duration = models.IntegerField()
    description = models.TextField(
        null=True,
        blank=True
    )
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
        blank=True
    )
    languages = models.ManyToManyField(
        Language,
        related_name='movies',
        blank=True
    )
    genres = models.ManyToManyField(
        Genre,
        related_name='movies',
        blank=True
    )

    def __str__(self):
        return f'{self.title} {self.release_year}'


# TODO: Create a logic for changing seasons fields base on every season object added to this series or a function
class Series(models.Model):
    title = models.CharField(max_length=255)
    release_year = models.IntegerField()
    end_date = models.DateField(
        null=True,
        blank=True
    )
    description = models.TextField(
        null=True,
        blank=True
    )
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
        blank=True
    )
    languages = models.ManyToManyField(
        Language,
        related_name='series',
        blank=True
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='series',
        blank=True
    )

    def __str__(self):
        return self.title

    # def seasons(self):
        # return self.seasons


# TODO: Add a function for episodes of season
class Season(models.Model):
    title = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )
    number = models.IntegerField()

    series = models.ForeignKey(
        Series,
        on_delete=models.CASCADE,
        related_name='seasons'
    )
    avg_duration = models.IntegerField()
    release_year = models.IntegerField()
    description = models.TextField(
        null=True,
        blank=True
    )

    def __str__(self):
        season = str(self.number).zfill(3)
        return f"{self.series}: {self.title or ''} (S{season})"


class Episode(models.Model):
    title = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )
    season = models.ForeignKey(
        Season,
        on_delete=models.CASCADE,
        related_name='episodes',
    )
    number = models.IntegerField()
    duration = models.IntegerField(
        null=True,
        blank=True
    )
    description = models.TextField(
        null=True,
        blank=True
    )

    def __str__(self):
        season = str(self.season.number).zfill(3)
        episode = str(self.number).zfill(3)
        return f"{self.season.series}: {self.title or ''} (S{season}E{episode})"


class DownloadFile(models.Model):
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
    )
    quality = models.CharField(
        max_length=20,
        choices=QualityChoices.choices
    )
    download_url = models.TextField(
        null=True,
        blank=True
    )

    def __str__(self):
        context = f"Movie: {self.movie.title}"\
            if self.movie\
            else f"Episode: {self.episode.title} (S{self.episode.season}E{self.episode.number})" \
            if self.episode\
            else "No Context"

        file_name = self.file.name.split('/')[-1] if self.file else "No File"
        return f"{context} | Quality: {self.quality} | File: {file_name}"

    def save(self, *args, **kwargs):
        if not self.episode and not self.movie:
            raise ValueError(
                "Download File must be associated with either a movie or a series.")
        if self.episode and self.movie:
            raise ValueError(
                "Download File cannot be associated with both a movie and a series simultaneously.")
        return super().save(*args, **kwargs)


class Subtitle(models.Model):
    title = models.CharField(
        null=True,
        blank=True
    )
    language = models.ForeignKey(
        Language,
        on_delete=models.DO_NOTHING,
        related_name='subtitles'
    )
    file = models.FileField(upload_to='media/subtitles/')
    download_file = models.ForeignKey(
        DownloadFile,
        on_delete=models.CASCADE,
        related_name='subtitles',
    )

    def __str__(self):
        return f"Subtitle ({self.language}) for {self.download_file.quality}"



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
        on_delete=models.CASCADE,
        related_name='trailers',
        null=True,
        blank=True
    )
    series_season = models.ForeignKey(
        Season,
        on_delete=models.CASCADE,
        related_name='trailers',
        null=True,
        blank=True
    )

    def __str__(self):
        if self.movie:
            if self.title:
                return f"Trailer for Movie: {self.movie} - {self.title}"
            else:
                return f"Trailer for Movie: {self.movie}"

        elif self.series_season:
            series_title = self.series_season.series
            season_number = f"Season {self.series_season.number:02}"
            if self.title:
                return f"Trailer for Series: {series_title} ({season_number}) - {self.title}"
            else:
                return f"Trailer for Series: {series_title} ({season_number})"

        return f"Trailer: {self.title}"

    def save(self, *args, **kwargs):
        if not self.series_season and not self.movie:
            raise ValueError(
                "Trailer must be associated with either a movie or a series.")
        if self.series_season and self.movie:
            raise ValueError(
                "Trailer cannot be associated with both a movie and a series simultaneously.")
        return super().save(*args, **kwargs)
