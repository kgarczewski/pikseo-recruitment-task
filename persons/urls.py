from django.urls import path

from persons.views import main, SkillList

app_name = "persons"
urlpatterns = [
    path("", main, name="main"),
    path("skills", SkillList.as_view(), name="skills")
]
