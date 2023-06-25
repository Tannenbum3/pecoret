from django.db import models
from .base import BaseAsset


class Host(BaseAsset):
    ip = models.GenericIPAddressField()
    dns = models.CharField(max_length=255, null=True, blank=True)
    operating_system = models.CharField(max_length=255, null=True, blank=True)

    asset_type = "host"

    class Meta:
        ordering = ["-pk"]
        constraints = [
            models.UniqueConstraint(
                fields=["project", "ip"], name="host_ip_unique"
            )
        ]

    @property
    def get_asset_type_display(self):
        return "Host"

    @property
    def name(self):
        return self.__str__()

    def __str__(self):
        if not self.dns:
            return self.ip
        return f"{self.dns} ({self.ip})"
