from django.core.management.base import BaseCommand
from django.db import transaction
from faker import Faker
from persons.models import Persons, Position, Skills
import random


fake = Faker("pl_PL")

_skills = [
    "Python", "Django", "Java", "JavaScript", "Html", "Css", "Flask", "Htmx", "Linux"
]


def _unique_positions():
    positions = []
    while len(positions) < 20:
        job = fake.job()
        if job not in positions:
            yield job
            positions.append(job)


class Command(BaseCommand):

    @transaction.atomic()
    def handle(self, *args, **options):

        positions_to_create = []
        for position in _unique_positions():
            positions_to_create.append(Position(name=position))

        Position.objects.bulk_create(positions_to_create)

        skills_to_create = []
        for skill in _skills:
            skills_to_create.append(Skills(name=skill))

        Skills.objects.bulk_create(skills_to_create)

        persons_to_create = []
        for _ in range(100):
            persons_to_create.append(
                Persons(
                    first_name=fake.first_name(),
                    last_name=fake.last_name(),
                    position=random.choice(positions_to_create),
                )
            )

        Persons.objects.bulk_create(persons_to_create)

        for person in persons_to_create:
            for skill in random.choices(skills_to_create, k=3):
                person.skills.add(skill)

            person.save()

