from django.contrib import admin

from persons.models import Persons, Position, Skills
from django.db.models import QuerySet
from typing import Any, Optional

@admin.register(Persons)
class PersonsAdmin(admin.ModelAdmin):
    list_display = (
        "first_name",
        "last_name",
        "position",
        "display_skills",
        "age",
    )
    list_filter = ("position", "skills", "age")
    search_fields = ("first_name", "last_name")

    def display_skills(self, obj: Persons) -> str:
        """Returns the skills associated with a person as a comma-separated list."""
        return ", ".join([skill.name for skill in obj.skills.all()])

    display_skills.short_description = "Skills"

    def get_queryset(self, request: Any) -> QuerySet:
        """
        Optimizes the queryset for the Persons admin list view by prefetching
        related data.
        """
        queryset = super().get_queryset(request)
        queryset = queryset.prefetch_related("skills").select_related("position")
        return queryset


@admin.register(Skills)
class SkillsAdmin(admin.ModelAdmin):
    list_display = ("name", "number_of_persons")
    search_fields = ("name",)

    def number_of_persons(self, obj: Skills) -> int:
        """
        Returns the count of persons associated with a skill.

        This method calculates the number of persons linked to a particular skill via the
        ManyToMany relationship. Useful for understanding the popularity of skills among
        persons.
        """
        return obj.persons_set.count()

    number_of_persons.short_description = "Number of Persons"


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ("name", "number_of_persons")
    search_fields = ("name",)

    def number_of_persons(self, obj: Position) -> int:
        """
        Returns the count of persons currently occupying a position.

        Provides a count of how many persons are associated with each position,
        which helps in assessing the utilization of positions across the organization.
        """
        return obj.persons_set.count()

    number_of_persons.short_description = "Number of Persons"
