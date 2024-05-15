import csv

from django.core.management import BaseCommand, CommandError
from ingredients.models import Ingredients


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument(
            "csv_file",
            type=str,
            help="Path to the CSV file containing ingredients data",
        )

    def handle(self, *args, **options):
        csv_file_path = options["csv_file"]
        try:
            with open(csv_file_path, "r", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    Ingredients.objects.get_or_create(
                        name=row["name"],
                        measurement_unit=row["measurement_unit"],
                    )
                self.stdout.write(
                    self.style.SUCCESS("Successfully imported ingredients")
                )
        except FileNotFoundError:
            raise CommandError(
                'File "{}" does not exist'.format(csv_file_path)
            )
        except csv.Error:
            raise CommandError(
                'File "{}" is not a valid CSV file'.format(csv_file_path)
            )
