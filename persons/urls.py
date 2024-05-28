from django.urls import path

from persons.views import AgeUpdateView, PersonsListView, SkillList, main

app_name = "persons"
urlpatterns = [
    path("", main, name="main"),
    path("skills", SkillList.as_view(), name="skills"),
    path("update_age", AgeUpdateView.as_view(), name="update_age"),
    path("persons_list", PersonsListView.as_view(), name="age_list"),
]
