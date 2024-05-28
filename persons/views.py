from django.shortcuts import render
from django.views.generic import ListView

from persons.models import Skills


def main(request):
    return render(request, template_name="main.html")


class SkillList(ListView):
    queryset = Skills.objects.all()
    template_name = "skills.html"
    context_object_name = "skills"
