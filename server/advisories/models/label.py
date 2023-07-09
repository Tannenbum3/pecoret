import colorsys
from django.db import models
from django.core.validators import RegexValidator
from pecoret.core.models import PeCoReTBaseModel, TimestampedModel


class Label(PeCoReTBaseModel, TimestampedModel):
    name = models.CharField(max_length=128, unique=True)
    description = models.TextField(null=True, blank=True)
    color = models.CharField(max_length=7, validators=[
        RegexValidator(regex=r'#([a-fA-F\d]{6}|[a-fA-F\d]{3})')
    ])

    def __str__(self):
        return self.name

    @property
    def color_rgb(self):
        return tuple(int(self.color.lstrip("#")[i:i + 2], 16) for i in (0, 2, 4))

    @property
    def color_hsl(self):
        r, g, b = self.color_rgb
        return colorsys.rgb_to_hsv(r, g, b)

    class Meta:
        ordering = ["name"]
