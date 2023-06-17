from django.db import models
from .assets import AssetRelatedModel


class PeCoReTBaseModel(models.Model):
    """a base model that can be used to always perform full_clean on save
    """
    class Meta:
        abstract = True

    def pre_save(self):
        pass

    def post_save(self):
        pass

    def save(self, *args, **kwargs):
        """always do a `full_clean` on save
        """
        self.pre_save()
        self.full_clean(validate_unique=False)
        super().save(*args, **kwargs)
        self.post_save()

class TimestampedModel(models.Model):
    """model which just tracks dates for udpate and create
    """
    date_created = models.DateTimeField(auto_now_add=True, null=False, blank=False)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ["-date_created", "-date_updated"]
