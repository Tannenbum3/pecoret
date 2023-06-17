import uuid
import base64
from pathlib import Path
from django.db import models
from pecoret.core.models import TimestampedModel


class ProofQuerySet(models.QuerySet):
    def for_finding(self, finding):
        return self.filter(finding=finding)

    def for_project_finding(self, finding, project):
        return self.filter(finding=finding, finding__project=project)

    def for_project(self, project):
        return self.filter(finding__project=project)


def project_proof_path(instance, filename):
    return f"uploads/projects/{instance.project.pk}/proofs/{instance.finding.pk}_{uuid.uuid4()}{Path(filename).suffix}"


class Proof(TimestampedModel):
    objects = ProofQuerySet.as_manager()
    finding = models.ForeignKey('backend.Finding', on_delete=models.CASCADE)
    title = models.CharField(max_length=256)
    order = models.PositiveSmallIntegerField(null=True)
    text = models.TextField(null=True, blank=True)
    image = models.ImageField(max_length=256, null=True, blank=True, upload_to=project_proof_path)
    image_caption = models.CharField(max_length=256, null=True, blank=True)


    class Meta:
        ordering = ["finding", "order"]
        unique_together = [
            ('finding', 'title')
        ]

    @property
    def project(self):
        return self.finding.project

    def __str__(self):
        return self.title

    @property
    def image_base64(self):
        if not self.image:
            return ""
        with open(self.image.path, "rb") as image_f:
            encoded = base64.b64encode(image_f.read())
            return encoded.decode()

    def base64_encoded_image(self):
        return "data:image/png;base64, %s" % self.image_base64

    def delete(self, using=None, keep_parents=False):
        self.image.delete()
        super().delete(using=using, keep_parents=keep_parents)
