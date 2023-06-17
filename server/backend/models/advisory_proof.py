import uuid
import base64
from pathlib import Path
from django.db import models
from pecoret.core.models import TimestampedModel


class ProofQuerySet(models.QuerySet):
    def for_advisory(self, advisory):
        return self.filter(advisory=advisory)


def advisory_proof_upload_path(instance, filename):
    return f"uploads/advisories/{instance.advisory.pk}/proofs/{uuid.uuid4()}{Path(filename).suffix}"


class AdvisoryProof(TimestampedModel):
    objects = ProofQuerySet.as_manager()
    advisory = models.ForeignKey('backend.Advisory', on_delete=models.CASCADE)
    title = models.CharField(max_length=256)
    order = models.PositiveSmallIntegerField(null=True)
    text = models.TextField(null=True, blank=True)
    image = models.ImageField(max_length=256, null=True, blank=True, upload_to=advisory_proof_upload_path)
    image_caption = models.CharField(max_length=256, null=True, blank=True)

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

    class Meta:
        ordering = ["advisory", "order"]
