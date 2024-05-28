# Create your tests here.
import csv
import os
from unittest.mock import patch

import pytest
from django.core.management import call_command
from django.urls import reverse

from persons.forms import NameForm
from persons.models import Persons, Position, Skills


@pytest.mark.django_db
def test_persons_model():
    """
    Test the creation and attribute setting of the Persons model.
    """
    person = Persons.objects.create(first_name="John", last_name="Doe", age=25)
    assert person.age == 25


@pytest.mark.django_db(transaction=True)
def test_name_form():
    """
    Test the NameForm to ensure it only includes unique names from the Persons model.
    """

    # Clean up the database before the test
    Persons.objects.all().delete()

    # Create test data
    Persons.objects.create(first_name="John", last_name="Doe")
    Persons.objects.create(first_name="Jane", last_name="Doe")
    Persons.objects.create(first_name="John", last_name="Smith")

    # Create and validate the form
    form = NameForm()
    choices = dict(form.fields["name"].choices)
    assert "John" in choices.keys()
    assert "Jane" in choices.keys()
    assert len(choices) == 2  # Ensure no duplicates


@pytest.mark.django_db
def test_age_update_view_get(client):
    """
    Test the AgeUpdateView GET request to ensure the form is rendered correctly.
    """
    response = client.get(reverse("persons:update_age"))
    assert response.status_code == 200
    assert "form" in response.context


@pytest.mark.django_db
@patch("requests.get")
def test_age_update_view_post(mock_get, client):
    """
    Test the AgeUpdateView POST request to ensure it updates the age via the external API.
    """

    Persons.objects.create(first_name="John", last_name="Doe")
    mock_get.return_value.json.return_value = {"name": "John", "age": 30}

    response = client.post(reverse("persons:update_age"), {"name": "John"})

    assert response.status_code == 302  # Redirect after POST
    assert response.url == reverse("persons:age_list")

    # Verify the age has been updated
    person = Persons.objects.get(first_name="John")
    assert person.age == 30


@pytest.mark.django_db
def test_persons_list_view(client):
    """
    Test the PersonsListView to ensure it displays persons sorted by age correctly.
    """
    Persons.objects.create(first_name="John", last_name="Doe", age=25)
    Persons.objects.create(first_name="Jane", last_name="Doe", age=20)
    Persons.objects.create(first_name="Bob", last_name="Smith")  # No age

    response = client.get(reverse("persons:age_list"))

    assert response.status_code == 200
    persons = response.context["persons"]
    assert len(persons) == 2  # Only two persons with age specified
    assert persons[0].first_name == "Jane"
    assert persons[1].first_name == "John"


@pytest.mark.django_db(transaction=True)
def test_export_persons_data(tmpdir):
    """
    Test the export_persons_data management command to ensure it exports the correct
    data to a CSV file.
    """
    # Clean up the database before the test
    Skills.objects.all().delete()
    Position.objects.all().delete()
    Persons.objects.all().delete()

    # Setup test data
    skill1 = Skills.objects.create(name="Python")
    skill2 = Skills.objects.create(name="Django")
    position = Position.objects.create(name="Developer")

    person1 = Persons.objects.create(
        first_name="John", last_name="Doe", position=position
    )
    person1.skills.add(skill1, skill2)

    person2 = Persons.objects.create(
        first_name="Jane", last_name="Doe", position=position
    )
    person2.skills.add(skill1)

    # Set the file path to a temporary directory
    output_file = tmpdir.join("persons_data.csv")

    # Execute the command with the temporary file path
    call_command(
        "export_persons_data", file_path=str(output_file), stdout=open(os.devnull, "w")
    )

    # Verify the contents of the CSV file
    with open(str(output_file), "r") as f:
        reader = csv.reader(f)
        rows = list(reader)

    # Check the header
    assert rows[0] == ["Lp.", "Imię", "Nazwisko", "Umiejętności", "Pozycja"]

    # Check the data
    assert rows[1] == ["1", "John", "Doe", "Python, Django", "Developer"]
    assert rows[2] == ["2", "Jane", "Doe", "Python", "Developer"]
