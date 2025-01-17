from django.core.management.base import BaseCommand
from model_bakery import baker
from faker import Faker  # type: ignore
from movie.models import Genre, Language, Country


faker = Faker()


class Command(BaseCommand):
    help = "Populate the database with test data for Genre, Language, Country"

    def handle(self, *args, **kwargs):
        # Create Countries
        self.stdout.write("Creating Countries...")
        countries = baker.make(
            Country,
            _quantity=30,
            name=lambda: faker.unique.country()
        )

        # Create Languages
        self.stdout.write("Creating Languages...")
        languages = baker.make(
            Language,
            _quantity=30,
            name=lambda: faker.unique.language_name()
        )

        # Create Genres
        self.stdout.write("Creating Genres...")
        genres = baker.make(
            Genre,
            _quantity=30,
            name=lambda: faker.unique.word().capitalize()
        )
