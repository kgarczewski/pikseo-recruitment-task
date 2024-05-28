from django import forms

from .models import Persons


class NameForm(forms.Form):
    """
    A Django form for selecting a unique first name from the Persons model.

    This form is used to select a name from a dropdown list of unique first names present
    in the database. It dynamically retrieves and lists all unique first names from
    the Persons model upon initialization, ensuring that the dropdown always reflects
    the current database entries without duplicates.
    """

    def __init__(self, *args, **kwargs):
        super(NameForm, self).__init__(*args, **kwargs)
        unique_names = (
            Persons.objects.values_list("first_name", flat=True)
            .order_by("first_name")
            .distinct()
        )
        self.fields["name"] = forms.ChoiceField(
            choices=[(name, name) for name in unique_names]
        )
