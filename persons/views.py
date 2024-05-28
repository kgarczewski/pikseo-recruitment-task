import requests
from django.db.models import Prefetch, QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import ListView

from persons.models import Persons, Skills

from .forms import NameForm


def main(request):
    return render(request, template_name="main.html")


class SkillList(ListView):
    template_name = "skills.html"
    context_object_name = "skills"

    def get_queryset(self) -> QuerySet:
        """
        Prefetch the persons_set and, using select_related, also fetch the related
        position for each person to solve the N+1 query issue.
        """
        return Skills.objects.prefetch_related(
            Prefetch("persons_set", queryset=Persons.objects.select_related("position"))
        )


class AgeUpdateView(View):
    """
    View to handle the age update form and API interaction.

    This view serves an age update form on GET request and processes the form on POST
    request. Upon form submission, it fetches the age of a person from an external API
    using the provided name, updates this age in the database, and redirects to a list
    of all persons sorted by age.
    """

    template_name = "age_form.html"

    def get(self, request: HttpRequest) -> HttpResponse:
        """
        Handle GET requests: render the form for age update.
        """
        form = NameForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request: HttpRequest) -> HttpResponse:
        """
        Handle POST requests: process the age update form.

        Validates the form, fetches the age using an external API, updates the age in
        the database for all matching records, and redirects to the age list view.
        """
        form = NameForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            response = requests.get(f"https://api.agify.io/?name={name}")
            data = response.json()
            age = data.get("age")
            Persons.objects.filter(first_name=name).update(age=age)
            return redirect("persons:age_list")
        return render(request, self.template_name, {"form": form})


class PersonsListView(ListView):
    """
    View to display a list of persons sorted by their age.

    This view lists persons excluding those without an age specified, sorted in ascending
    order by age. It utilizes Django's generic ListView for displaying the sorted list.
    """

    model = Persons
    template_name = "persons_list.html"
    context_object_name = "persons"
    queryset = Persons.objects.exclude(age__isnull=True).order_by("age")
