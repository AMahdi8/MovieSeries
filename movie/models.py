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


class Crew(models.Model):
    ROLE_CHOICES = (
        ('A', 'Actor'),
        ('D', 'Director'),
        ('W', 'Writer'),
        ('O', 'Other')
    )
    name = models.CharField(max_length=255)
    role = models.CharField(max_length=1, choices=ROLE_CHOICES)
    bio = models.TextField()
    birth_date = models.DateField()
    image = models.ImageField(
        upload_to='media/images/crews/',
        null=True,
        blank=True
    )
    country = models.ForeignKey(
        Country,
        on_delete=models.DO_NOTHING,
        related_name='actors',
        null=True,
        blank=True
    )

    def __str__(self):
        return self.name


class Movie(models.Model):
    AGE_CATEGORY_CHOICES = (
        ('G', 'General Audiences'),
        ('PG', 'Parental Guidance Suggested'),
        ('PG-13', 'Parents Strongly Cautioned'),
        ('R', 'Restricted'),
        ('NC-17', 'Adults Only')
    )
    title = models.CharField(max_length=255)
    release_year = models.IntegerField()
    duration = models.IntegerField()
    age_category = models.CharField(max_length=5, choices=AGE_CATEGORY_CHOICES)
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
    crews = models.ManyToManyField(
        Crew,
        related_name='movies',
        blank=True
    )

    @property
    def average_rating(self):
        ratings = self.comments.exclude(
            rating=None).values_list('rating', flat=True)
        return sum(ratings) / len(ratings) if ratings else None

    @property
    def comments_count(self):
        return self.comments.count()

    def __str__(self):
        return f'{self.title} {self.release_year}'


# TODO: Create a logic for changing seasons fields base on every season object added to this series or a function
class Series(models.Model):
    AGE_CATEGORY_CHOICES = (
        ('G', 'General Audiences'),
        ('PG', 'Parental Guidance Suggested'),
        ('PG-13', 'Parents Strongly Cautioned'),
        ('R', 'Restricted'),
        ('NC-17', 'Adults Only')
    )
    title = models.CharField(max_length=255)
    release_year = models.IntegerField()
    end_date = models.IntegerField(
        null=True,
        blank=True
    )
    age_category = models.CharField(max_length=5, choices=AGE_CATEGORY_CHOICES)
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
    image = models.ImageField(
        upload_to='media/images/series/',
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
    genres = models.ManyToManyField(
        Genre,
        related_name='series',
        blank=True
    )
    crews = models.ManyToManyField(
        Crew,
        related_name='series',
        blank=True
    )

    @property
    def average_rating(self):
        ratings = self.comments.exclude(
            rating=None).values_list('rating', flat=True)
        return sum(ratings) / len(ratings) if ratings else None

    @property
    def comments_count(self):
        return self.comments.count()

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

    SOURCE_CHOICES = [
        ('WEB-DL', 'WEB-DL'),
        ('WEBRip', 'WEBRip'),
        ('Blu-ray', 'Blu-ray'),
        ('BRRip', 'BRRip'),
        ('HDRip', 'HDRip'),
        ('DVD-Rip', 'DVD-Rip'),
        ('CAM', 'CAM'),
        ('TS', 'TS'),
        ('HDTV', 'HDTV'),
    ]

    FILE_FORMAT_CHOICES = [
        ('MP4', 'MP4'),
        ('FLV', 'FLV'),
        ('MOV', 'MOV'),
        ('MKV', 'MKV'),
        ('LXF', 'LXF'),
        ('MXF', 'MXF'),
        ('AVI', 'AVI'),
        ('QuickTime', 'QuickTime'),
        ('WebM', 'WebM'),
    ]

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
        upload_to='media/videos/',
    )
    source = models.CharField(
        max_length=20,
        choices=SOURCE_CHOICES,
        default='WEB-DL',
        help_text="Source of the video file."
    )
    file_format = models.CharField(
        max_length=20,
        choices=FILE_FORMAT_CHOICES,
        default='MP4',
        help_text="File container format."
    )
    sticky_subtitles = models.BooleanField()
    quality = models.CharField(
        max_length=20,
        choices=QualityChoices.choices
    )
    download_url = models.TextField(
        null=True,
        blank=True
    )

    @property
    def file_size(self):
        if self.file and self.file.name:
            return self.file.size
        return None

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
    download_link = models.TextField(
        null=True,
        blank=True
    )
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

    trailer_video = models.FileField(
        upload_to='media/trailers/',
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
