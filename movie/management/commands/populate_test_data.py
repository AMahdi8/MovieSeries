from django.core.management.base import BaseCommand
from faker import Faker  # type: ignore
from model_bakery import baker
from random import sample
from movie.models import Country, Language, Genre, Crew, Movie, Series, Season, Episode, DownloadFile
import tempfile


class Command(BaseCommand):
    help = "Populate the database with test data."

    def handle(self, *args, **kwargs):
        faker = Faker()

        # Create Countries
        self.stdout.write("Creating Countries...")
        countries = baker.make(
            Country,
            _quantity=10,
            name=lambda: faker.unique.country()
        )

        # Create Languages
        self.stdout.write("Creating Languages...")
        languages = baker.make(
            Language,
            _quantity=10,
            name=lambda: faker.unique.language_name()
        )

        # Create Genres
        self.stdout.write("Creating Genres...")
        genres = baker.make(
            Genre,
            _quantity=10,
            name=lambda: faker.unique.word().capitalize()
        )

        # Create Crews
        self.stdout.write("Creating Crews...")
        crews = []
        for _ in range(20):
            img_content = faker.image()
            image_file = tempfile.NamedTemporaryFile(
                delete=False, suffix='.jpg')
            image_file.write(img_content)
            image_file.close()

            crew = baker.make(
                Crew,
                name=faker.name(),
                role=faker.random_element(['A', 'D', 'W', 'O']),
                bio=faker.text(max_nb_chars=200),
                birth_year=faker.random_int(min=1930, max=2025),
                country=faker.random_element(countries),
                image=image_file.name
            )
            crews.append(crew)

        # Create Movies
        self.stdout.write("Creating Movies...")
        movies = []
        for _ in range(40):
            movie = baker.make(
                Movie,
                title=faker.sentence(nb_words=3),
                release_year=faker.year(),
                duration=faker.random_int(min=60, max=180),
                age_category=faker.random_element(
                    ['G', 'PG', 'PG-13', 'R', 'NC-17']),
                description=faker.text(max_nb_chars=500),
                imdb_rank=faker.random_int(min=1, max=250),
                rate=faker.pydecimal(
                    left_digits=1, right_digits=1, min_value=1, max_value=10),
                subtitle_link=faker.text(max_nb_chars=500),
                trailer_link=faker.text(max_nb_chars=500),
            )

            movie.countries.add(*sample(countries, k=3))
            movie.languages.add(*sample(languages, k=2))
            movie.genres.add(*sample(genres, k=3))
            movie.crews.add(*sample(crews, k=5))

            # Add download links for movies
            for _ in range(4):
                download_file = baker.make(
                    DownloadFile,
                    movie=movie,
                    quality=faker.random_element(
                        DownloadFile.QualityChoices.values),
                    file_format=faker.random_element(['MP4', 'MKV', 'AVI']),
                    source=faker.random_element(['WEB-DL', 'Blu-ray', 'HDTV']),
                    sticky_subtitles=faker.boolean(),
                    download_url=faker.url()
                )

                # # Add subtitles
                # for _ in range(2):
                #     baker.make(
                #         Subtitle,
                #         download_file=download_file,
                #         language=faker.random_element(languages),
                #         file=None,
                #         download_link=faker.url()
                #     )

            # Add trailers
            # for _ in range(2):
            #     baker.make(
            #         Trailer,
            #         movie=movie,
            #         title=faker.sentence(nb_words=4),
            #         url=faker.url(),
            #         upload_date=faker.date_this_year(),
            #     )

            movies.append(movie)

        # Create Series
        self.stdout.write("Creating Series...")
        series_list = []
        for _ in range(30):
            series = baker.make(
                Series,
                title=faker.sentence(nb_words=3),
                release_year=faker.year(),
                description=faker.text(max_nb_chars=500),
                imdb_rank=faker.random_int(min=1, max=250),
                rate=faker.pydecimal(
                    left_digits=1, right_digits=1, min_value=1, max_value=10),
            )

            series.countries.add(*sample(countries, k=2))
            series.languages.add(*sample(languages, k=2))
            series.genres.add(*sample(genres, k=3))
            series.crews.add(*sample(crews, k=7))

            # Create Seasons
            for season_number in range(1, 4):  # Create 3 seasons per series
                season = baker.make(
                    Season,
                    series=series,
                    number=season_number,
                    trailer_link=faker.text(max_nb_chars=500),
                )

                # Add episodes to each season
                for episode_number in range(1, 11):  # 10 episodes per season
                    episode = baker.make(
                        Episode,
                        season=season,
                        number=episode_number,
                        title=faker.sentence(nb_words=4),
                        duration=faker.random_int(min=20, max=60),
                        description=faker.text(max_nb_chars=300),
                        subtitle_link=faker.text(max_nb_chars=500),
                    )

                    # Add download files for episodes
                    for _ in range(2):
                        download_file = baker.make(
                            DownloadFile,
                            episode=episode,
                            quality=faker.random_element(
                                DownloadFile.QualityChoices.values),
                            file_format=faker.random_element(
                                ['MP4', 'MKV', 'AVI']),
                            source=faker.random_element(
                                ['WEB-DL', 'Blu-ray', 'HDTV']),
                            sticky_subtitles=faker.boolean(),
                            download_url=faker.url()
                        )

                        # # Add subtitles
                        # for _ in range(2):
                        #     baker.make(
                        #         Subtitle,
                        #         download_file=download_file,
                        #         language=faker.random_element(languages),
                        #         file=None,
                        #         download_link=faker.url()
                        #     )

                # Add trailers for the season
                # for _ in range(2):
                #     baker.make(
                #         Trailer,
                #         series_season=season,
                #         title=faker.sentence(nb_words=4),
                #         url=faker.url(),
                #         upload_date=faker.date_this_year(),
                #     )

            series_list.append(series)

        self.stdout.write(f"Database populated successfully with:\n"
                          f"- {len(countries)} countries\n"
                          f"- {len(languages)} languages\n"
                          f"- {len(genres)} genres\n"
                          f"- {len(crews)} crew members\n"
                          f"- {len(movies)} movies\n"
                          f"- {len(series_list)} series")
