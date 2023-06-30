from django.db import models
from django.utils import timezone
from django.conf import settings
from django.dispatch import receiver
from pecoret.core.models import TimestampedModel
from .finding import Severity
from .vulnerability import VulnerabilityTemplate
from .advisory_timeline import AdvisoryTimeline
from .advisory_proof import AdvisoryProof, advisory_proof_upload_path
from .advisory_membership import AdvisoryMembership, Roles


def create_advisory_id():
    year = timezone.now().year
    qs = Advisory.objects.filter(
        date_created__date__year=year, advisory_id__isnull=False
    ).order_by("advisory_id")
    # first advisory this year
    if not qs.exists():
        return f"{year}-0001"
    last_id = qs.last().pk.split("-")[-1]
    length = len(str(last_id))
    if length < 4:
        formatter = "%04d"
    else:
        formatter = "%0{len}d".format(len=length)
    new_pk = formatter % int(int(last_id) + 1)
    return f"{year}-{new_pk}"


class AdvisoryStatusChoices(models.IntegerChoices):
    OPEN = 1, "Open"
    FIXED = 2, "Fixed"
    WONT_FIX = 3, "Wont Fix"


class AdvisoryQuerySet(models.QuerySet):
    def for_user(self, user):
        return self.filter(advisorymembership__user=user)

    def for_advisory_management(self, include_user=None):
        if not include_user:
            return self.filter(is_draft=False)
        return self.filter(
            models.Q(advisorymembership__user=include_user) | models.Q(is_draft=False)
        ).distinct()


class AdvisoryManager(models.Manager):
    def create_from_template(self, **data):
        data["date_planned_disclosure"] = timezone.now() + timezone.timedelta(days=60)
        data["recommendation"] = VulnerabilityTemplate.objects.get(
            vulnerability_id=data["vulnerability_key"]
        ).recommendation
        advisory = self.create(**data)
        return advisory

    def create_from_finding(self, finding, **data):
        data["date_planned_disclosure"] = timezone.now() + timezone.timedelta(days=60)
        data["severity"] = finding.severity
        data["user"] = finding.user
        data["internal_name"] = finding.name
        data["vulnerability"] = VulnerabilityTemplate.objects.get(
            vulnerability_id=finding.vulnerability.vulnerability_id
        )
        advisory = self.create(**data)
        if finding.recommendation:
            advisory.recommendation = finding.recommendation
        else:
            advisory.recommendation = finding.vulnerability.recommendation
        for proof in finding.proof_set.all():
            if proof.image:
                with open(self.image.path, "rb") as image_f:
                    image_data = image_f.read()
                advisory_proof = AdvisoryProof.objects.create(
                    title=proof.title,
                    text=proof.title,
                    advisory=advisory,
                    image_caption=proof.caption,
                )
                advisory_proof_image_path = advisory_proof_upload_path(
                    advisory_proof, "proof.png"
                )
                with open(advisory_proof_image_path, "wb") as image_f:
                    image_f.write(image_data)
                advisory_proof.image = advisory_proof_image_path
                advisory_proof.save()
            else:
                AdvisoryProof.objects.create(
                    title=proof.title, advisory=advisory, text=proof.text
                )
        return advisory


class Advisory(TimestampedModel):
    # pylint: disable=missing-class-docstring
    objects = AdvisoryManager.from_queryset(AdvisoryQuerySet)()
    advisory_id = models.CharField(
        max_length=28, primary_key=True, default=create_advisory_id
    )
    user = models.ForeignKey("backend.User", on_delete=models.PROTECT)
    date_planned_disclosure = models.DateField()
    date_disclosure = models.DateField(blank=True, null=True)
    product = models.CharField(max_length=128)
    internal_name = models.CharField(max_length=64, default="")
    status = models.PositiveSmallIntegerField(
        choices=AdvisoryStatusChoices.choices, default=AdvisoryStatusChoices.OPEN
    )
    affected_versions = models.CharField(max_length=128)
    fixed_version = models.CharField(max_length=128, blank=True, null=True)
    vulnerability = models.ForeignKey(
        "backend.VulnerabilityTemplate", on_delete=models.PROTECT
    )
    severity = models.PositiveSmallIntegerField(choices=Severity.choices)
    cve_id = models.CharField(max_length=20, null=True, blank=True)
    is_draft = models.BooleanField(default=True)
    vendor_url = models.URLField()
    vendor_name = models.CharField(max_length=128)
    description = models.TextField(null=True, blank=True)
    recommendation = models.TextField(null=True, blank=True)
    labels = models.ManyToManyField('advisories.Label', blank=True)

    def __str__(self):
        return self.advisory_id

    def get_advisory_id_display(self):
        return f"{settings.ADVISORY_ID_PREFIX}{self.advisory_id}"

    @property
    def vulnerability_key(self):
        return self.vulnerability.natural_key

    @vulnerability_key.setter
    def vulnerability_key(self, value):
        self.vulnerability = VulnerabilityTemplate.objects.get(vulnerability_id=value)

    class Meta:
        ordering = ["-advisory_id", "date_updated"]


@receiver(models.signals.post_save, sender=Advisory)
def on_advisory_create(sender, instance, created, **kwargs):
    if created:
        AdvisoryTimeline.objects.create(
            date=timezone.now(), text="Advisory created", advisory=instance
        )
        # creators should not have expiry date
        AdvisoryMembership.objects.create(
            user=instance.user, role=Roles.CREATOR, advisory=instance
        )
