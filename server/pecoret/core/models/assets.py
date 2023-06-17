from django.db import models
from django.core.exceptions import ValidationError


class AssetRelatedModel(models.Model):
    assets = ["web_application", "host", "service"]

    project = models.ForeignKey(
        "backend.Project", editable=False, on_delete=models.CASCADE
    )

    web_application = models.ForeignKey(
        "backend.WebApplication", on_delete=models.CASCADE, null=True, blank=True
    )
    host = models.ForeignKey(
        "backend.Host", on_delete=models.CASCADE, null=True, blank=True
    )
    service = models.ForeignKey(
        "backend.Service", on_delete=models.CASCADE, null=True, blank=True
    )

    class Meta:
        abstract = True

    @property
    def asset(self):
        for asset in self.assets:
            if getattr(self, asset):
                return getattr(self, asset)
        return None

    @asset.setter
    def asset(self, value):
        for field, value in self.asset_field_values(value).items():
            setattr(self, field, value)

    def asset_field_values(self, value):
        found = False
        fields = {}
        for asset in self.assets:
            if isinstance(value, self._meta.get_field(asset).related_model):
                fields[asset] = value
                found = True
            else:
                fields[asset] = None
        if not found:
            raise ValueError(f"{value} is no a valid asset")
        return fields

    @property
    def asset_type(self):
        for asset in self.assets:
            if getattr(self, asset):
                return asset
        return None

    def clean(self):
        for asset in self.assets:
            if getattr(self, asset) and getattr(self, asset).project != self.project:
                raise ValidationError(
                    {asset: f"The {asset} does not belong to the project."}
                )
        if not self.asset:
            raise ValidationError({"asset": "This field is required!"})
        return super().clean()
