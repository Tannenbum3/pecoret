from django.db import models
from pecoret.core.models import PeCoReTBaseModel


class Profile(PeCoReTBaseModel):
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    name = models.CharField(unique=True)

    class Meta:
        ordering = ["name"]
