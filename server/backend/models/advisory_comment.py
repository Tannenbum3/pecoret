from django.db import models
from pecoret.core.models import TimestampedModel


class AdvisoryCommentQuerySet(models.QuerySet):
    def for_advisory(self, advisory):
        return self.filter(advisory=advisory)


class AdvisoryComment(TimestampedModel):
    objects = AdvisoryCommentQuerySet.as_manager()
    advisory = models.ForeignKey('backend.Advisory', on_delete=models.CASCADE)
    comment = models.TextField()
    user = models.ForeignKey('backend.User', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return str(self.advisory)

    class Meta:
        ordering = ["date_created"]
