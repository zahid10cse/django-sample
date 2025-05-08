from django.db import models


class Country(models.Model):
    name = models.CharField(max_length=100, unique=True)
    cca2 = models.CharField(max_length=100, null=True, blank=True)
    capital = models.CharField(max_length=100, null=True, blank=True)
    population = models.PositiveIntegerField(null=True, blank=True)
    timezone = models.CharField(max_length=100, null=True, blank=True)
    flag = models.TextField(null=True, blank=True)

    def __str__(self) -> str:
        return self.name + "-" + self.cca2

    class Meta:
        db_table = "countries"
