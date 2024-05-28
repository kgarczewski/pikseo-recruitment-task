import csv
from django.core.management.base import BaseCommand
from persons.models import Persons


class Command(BaseCommand):
    help = 'Export persons data along with their skills and positions to a CSV file'

    def add_arguments(self, parser):
        parser.add_argument(
            '--file_path',
            type=str,
            default='persons_data.csv',
            help='The file path for the CSV output'
        )

    def handle(self, *args, **kwargs):
        """
        Handle the command to export persons data to a CSV file.

        This method fetches all persons from the database, including their related
        skills and positions, and writes the data to a CSV file.
        Each person's skills are listed as a comma-separated string, and positions
        are included by name.
        """
        file_path = kwargs['file_path']

        # Open the CSV file for writing
        with open(file_path, 'w', newline='') as csvfile:
            # Create a CSV writer
            csvwriter = csv.writer(csvfile)

            # Write the header row
            csvwriter.writerow(['Lp.', 'Imię', 'Nazwisko', 'Umiejętności', 'Pozycja'])

            # Fetch all persons and write their data to the CSV file
            for idx, person in enumerate(
                    Persons.objects.prefetch_related('skills').select_related(
                            'position'), start=1):
                # Get the list of skills as a comma-separated string
                skills = ', '.join(skill.name for skill in person.skills.all())
                # Get the position name
                position = person.position.name if person.position else ''
                # Write the person's data to the CSV file
                csvwriter.writerow(
                    [idx, person.first_name, person.last_name, skills, position])

        self.stdout.write(
            self.style.SUCCESS(f'Successfully exported data to {file_path}'))
