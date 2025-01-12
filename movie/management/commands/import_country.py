import csv

from django.core.management.base import BaseCommand, CommandError
from movie.models import Country


class Command(BaseCommand):
    help = 'Storing Country objects from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('CSV_path', type=str,
                            help='The path to the CSV file')

    def handle(self, *args, **options):
        self.stdout.write("Importing countries")

        csv_path = options['CSV_path']

        try:
            with open(csv_path, newline='', mode='r', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    Country.objects.get_or_create(name=row[1][:-1])

        except FileNotFoundError:
            self.stderr.write(self.style.ERROR(
                f'File "{csv_path}" does not exist.'))

        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Error: {e}'))
