from django.db import models
from .assets.web_application import WebApplication
from .assets.host import Host


class AccountManager(models.Manager):
    def for_project(self, project):
        return self.filter(project=project)


class Account(models.Model):
    assets = ["web_application", "host"]
    web_application = models.ForeignKey(
        WebApplication,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    host = models.ForeignKey(Host, on_delete=models.CASCADE, null=True, blank=True)

    objects = AccountManager()
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    project = models.ForeignKey(
        "backend.Project", on_delete=models.CASCADE, editable=False
    )
    role = models.CharField(max_length=256, blank=True)
    username = models.CharField(max_length=256)
    password = models.CharField(max_length=256, blank=True)
    accessible = models.BooleanField(null=True, blank=True)
    compromised = models.BooleanField(default=False, blank=True)

    class Meta:
        ordering = ("-pk",)

    def __str__(self):
        return f"{self.username} in {self.asset}"

    @property
    def asset(self):
        for asset in self.assets:
            if getattr(self, asset):
                return getattr(self, asset)
        return None

    @asset.setter
    def asset(self, value):
        found = False
        for asset in self.assets:
            if isinstance(value, self._meta.get_field(asset).related_model):
                setattr(self, asset, value)
                found = True
            else:
                setattr(self, asset, None)
        if not found:
            raise ValueError(f"{value} is no a valid asset")
