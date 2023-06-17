from django.db import models
from .base import BaseAsset


class OperatingSystem(models.IntegerChoices):
    """Choices for the operating system of a mobile application
    """
    UNKNOWN = 0, "Unknown"
    ANDROID = 1, "Android"
    IOS = 2, "iOS"


class MobileApplication(BaseAsset):
    """Asset model for ``MobileApplication``.
    """
    name = models.CharField(max_length=256)
    version = models.CharField(max_length=128, blank=True)
    os = models.PositiveSmallIntegerField(
        choices=OperatingSystem.choices, default=OperatingSystem.UNKNOWN
    )
    certificate_pinning = models.BooleanField(null=True, blank=True)

    asset_type = "mobile_application"

    @property
    def get_asset_type_display(self):
        return "Mobile Application"

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name", "version"]
        unique_together = [("project", "name")]
