from django.db import models
from .base import BaseAsset


class WebApplication(BaseAsset):
    """Asset ``WebApplication``
    this asset is mainly used in web application pentests.
    """
    name = models.CharField(max_length=256)
    base_url = models.URLField()
    version = models.CharField(max_length=128, blank=True, null=True)

    asset_type = "web_application"

    class Meta:
        ordering = ["-pk"]
        unique_together = [
            ("project", "name")
        ]
        verbose_name = "Web Application"
        verbose_name_plural = "Web Applications"

    @property
    def get_asset_type_display(self):
        return self._meta.verbose_name

    def __str__(self):
        return self.name
