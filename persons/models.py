from django.db import models


class Skills(models.Model):
    name = models.CharField(verbose_name="Imię", max_length=64, unique=True)


class Position(models.Model):
    name = models.CharField(verbose_name="Stanowisko", max_length=64, unique=True)


class Persons(models.Model):
    first_name = models.CharField(verbose_name="Imię", max_length=64)
    last_name = models.CharField(verbose_name="Nazwisko", max_length=64)
    skills = models.ManyToManyField(Skills, verbose_name="Umiejętności")
    position = models.ForeignKey(
        Position, verbose_name="Stanowisko", null=True, on_delete=models.SET_NULL
    )
    age = models.IntegerField(verbose_name="Wiek", null=True, blank=True)
