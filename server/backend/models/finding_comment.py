from django.db import models
from pecoret.core.models import TimestampedModel


class FindingCommentQuerySet(models.QuerySet):
    def for_finding(self, finding):
        return self.filter(finding=finding)

    def for_project(self, project):
        return self.filter(finding__project=project)


class FindingComment(TimestampedModel):
    # TODO: CASCADE to set to a "Ghost" user as github does
    objects = FindingCommentQuerySet.as_manager()
    user = models.ForeignKey('backend.User', on_delete=models.PROTECT)
    comment = models.TextField()
    finding = models.ForeignKey('backend.Finding', on_delete=models.CASCADE)

    class Meta:
        ordering = ["date_created"]
