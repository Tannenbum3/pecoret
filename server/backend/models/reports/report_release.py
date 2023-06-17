from django.db import models
from django_q.models import Task as DjangoQTask
from pecoret.core.models import TimestampedModel


class ReleaseType(models.IntegerChoices):
    DRAFT = 0, "Draft"
    FINAL = 1, "Final"


class ReportReleaseManager(models.Manager):
    def for_project(self, project):
        return self.filter(report__project=project)


class ReportRelease(TimestampedModel):
    objects = ReportReleaseManager()
    name = models.CharField(max_length=128)
    raw_source = models.TextField(blank=True, null=True)
    compiled_source = models.BinaryField(blank=True, null=True)
    release_type = models.PositiveSmallIntegerField(choices=ReleaseType.choices)
    task_id = models.CharField(max_length=64, null=True, blank=True)
    report = models.ForeignKey('backend.Report', on_delete=models.CASCADE)
    content_type = models.CharField(max_length=128, default="application/octet-stream")
    file_extension = models.CharField(max_length=12, default="pdf")

    def __str__(self):
        return self.name

    @property
    def task(self):
        try:
            return DjangoQTask.objects.get(pk=self.task_id)
        except DjangoQTask.DoesNotExist:
            return DjangoQTask.objects.none()
