import re
from django.db import models
from django.utils import timezone
from django.conf import settings
from django.core.exceptions import ValidationError
from django.dispatch import receiver
from django.core.files.images import ImageFile
from pecoret.core.models import TimestampedModel
from .finding import Severity
from .vulnerability import VulnerabilityTemplate
from .advisory_timeline import AdvisoryTimeline
from .advisory_membership import AdvisoryMembership, Roles
from advisories.models.attachment import ImageAttachment


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

    def open(self):
        return self.filter(status=AdvisoryStatusChoices.OPEN)

    def fixed(self):
        return self.filter(status=AdvisoryStatusChoices.FIXED)

    def wont_fix(self):
        return self.filter(status=AdvisoryStatusChoices.WONT_FIX)

    def count_by_user(self):
        return self.values("user__username").annotate(count=models.Count('pk')).order_by("-count")


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
        data["proof_text"] = finding.proof_text
        data["internal_name"] = finding.name
        data["recommendation"] = finding.vulnerability.recommendation
        data["vulnerability"] = VulnerabilityTemplate.objects.get(
            vulnerability_id=finding.vulnerability.vulnerability_id
        )
        advisory = self.create(**data)
        if finding.recommendation:
            advisory.recommendation = finding.recommendation
        else:
            advisory.recommendation = finding.vulnerability.recommendation
        for proof in finding.findingimageattachment_set.all():
            image_file = ImageFile(proof.image)

            ImageAttachment.objects.create(
                caption=proof.caption,
                advisory=advisory,
                image=image_file
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
    custom_report_title = models.CharField(max_length=255, null=True, blank=True)
    hide_advisory_id_in_report = models.BooleanField(default=False)
    proof_text = models.TextField(blank=True, default="")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.old_is_draft = self.is_draft

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

    @property
    def report_proof_text(self):
        """
        to allow captions in the reports, we will inject some HTML,
        also we replace image with their base64 representation.
        we inject all these stuff in the markdown - before being rendered.
        This allows our injected data to be bleached before further used
        :return:
        """
        image_re = r'(?P<alt>!\[[^\]]*\])\((?P<filename>.*/advisories/\d+-\d+/attachments/(?P<attachment>\d+)/preview/+)(?=\"|\))\)'

        def attachment_replace(match):
            attachment_pk = match.group("attachment")
            qs = self.imageattachment_set.filter(pk=attachment_pk)
            if not qs.exists():
                # not an attachment for our finding! nice try!
                return match.group()
            attachment = qs.get()
            template = f"<div class='image-proof'><div class='image-container'><img src='{attachment.image_base64}'></div><div class='caption'><span class='figure-prefix'>Figure</span><span>{attachment.caption}</span></div></div>"
            return template

        proof_text = re.sub(image_re, attachment_replace, self.proof_text)
        return proof_text

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
