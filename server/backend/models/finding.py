import copy
from django.db import models
from django.db.models import signals
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from django.utils import timezone
from .vulnerability import Severity, ProjectVulnerability
from .cwe import CWE
from .finding_timeline import FindingTimeline
from .assets.web_application import WebApplication
from .assets.host import Host
from .assets.service import Service
from .assets.mobile_application import MobileApplication
from .cvss_score import CVSSBaseScore
from .owasp_risk_rating import OWASPRiskRating


class FindingStatus(models.IntegerChoices):
    OPEN = 0, _("Open")
    FIXED = 1, _("Fixed")
    WONT_FIX = 2, _("Wont Fix")


class FindingQuerySet(models.QuerySet):
    def for_project(self, project):
        return self.filter(project=project)

    def for_report(self, project):
        return self.for_project(project).filter(exclude_from_report=False)

    def with_asset(self, asset):
        kwargs = {asset.asset_type: asset.pk}
        return self.filter(**kwargs)

    def with_severity(self, severity_name):
        severity = Severity[severity_name.upper()]
        return self.filter(severity=severity)

    def is_fixed(self):
        return self.filter(status=FindingStatus.FIXED)


class FindingManager(models.Manager):
    def create_from_template(self, **data):
        cwe_ids_default = []
        template = None

        if "vuln_key" in data:
            template = ProjectVulnerability.objects.get_or_create_from_key(
                *data["vuln_key"]
            )
        elif "vulnerability" in data:
            template = data["vulnerability"]

        if template is not None:
            cwe_ids_default = template.cwe_id
            defaults_from_template = ["severity"]
            for key in defaults_from_template:
                data.setdefault(key, getattr(template, key))
        cwe_id = data.pop("cwe_ids", cwe_ids_default)
        finding = self.create(**data)
        finding.cwe_id = cwe_id
        return finding

    def copy_from_finding(self, finding):
        obj = self.model.objects.get(pk=finding.pk)
        obj.pk = None
        obj.save()
        for proof in finding.proof_set.all():
            new_proof = copy.copy(proof)
            new_proof.pk = None
            new_proof.finding = obj
            new_proof.save()
        return obj


class Finding(models.Model):
    objects = FindingManager.from_queryset(FindingQuerySet)()
    project = models.ForeignKey(
        "backend.Project", editable=False, on_delete=models.CASCADE
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    vulnerability = models.ForeignKey(
        "backend.ProjectVulnerability", on_delete=models.CASCADE
    )
    severity = models.PositiveSmallIntegerField(choices=Severity.choices)
    recommendation = models.TextField(blank=True, null=True)
    status = models.PositiveSmallIntegerField(
        choices=FindingStatus.choices, default=FindingStatus.OPEN
    )
    imported = models.BooleanField(default=False)
    finding_date = models.DateField(null=True, blank=True, default=None)
    name = models.CharField(max_length=256)
    authenticated_test = models.BooleanField(default=False)
    user_account = models.ForeignKey(
        "backend.Account", on_delete=models.SET_NULL, null=True, blank=True
    )
    needs_review = models.BooleanField(default=False)
    cwe_ids = models.ManyToManyField(CWE, blank=True)
    user = models.ForeignKey("backend.User", null=True, on_delete=models.SET_NULL)
    # retesting fields
    exclude_from_report = models.BooleanField(default=False)
    date_retest = models.DateField(null=True, blank=True)
    retest_results = models.TextField(null=True, blank=True)

    # assets
    assets = ["web_application", "host", "service", "mobile_application"]

    web_application = models.ForeignKey(
        WebApplication, on_delete=models.CASCADE, null=True, blank=True
    )
    mobile_application = models.ForeignKey(
        MobileApplication, on_delete=models.CASCADE, null=True, blank=True
    )
    host = models.ForeignKey(Host, on_delete=models.CASCADE, null=True, blank=True)
    service = models.ForeignKey(
        Service, on_delete=models.CASCADE, null=True, blank=True
    )

    class Meta:
        ordering = ["-severity"]

    def __str__(self):
        return f"{self.vulnerability.name} ({self.asset})"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.old_status = self.status

    @property
    def retested(self):
        if self.date_retest:
            return True
        return False

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

    def save(self, *args, **kwargs):
        if not self.finding_date:
            self.finding_date = timezone.now()
        if not self.pk or not self.project:
            self.project = self.vulnerability.project
        self.full_clean()
        return super().save(*args, **kwargs)

    def clean(self):
        # FIXME: remove workaround for django-admin which does model.clean on form submissions
        # Since finding.project is not yet set, this will through an error
        if not hasattr(self, "project"):
            self.project = self.vulnerability.project
        for asset in self.assets:
            if getattr(self, asset) and getattr(self, asset).project != self.project:
                raise ValidationError(
                    {
                        asset: f"The {asset} does not belong to the vulnerability's project."
                    }
                )
        if not self.asset:
            raise ValidationError({"asset": "is required"})
        return super().clean()

    @property
    def vuln_key(self):
        return self.vulnerability.natural_key

    @vuln_key.setter
    def vuln_key(self, value):
        self.vulnerability = ProjectVulnerability.objects.get_or_create_from_key(*value)

    @property
    def internal_id(self):
        return "{year}{project}{vuln}{finding}".format(
            year=self.project.year,
            project=self.project.pk,
            vuln=self.vulnerability.pk,
            finding=self.pk,
        )


@receiver(signals.post_save, sender=Finding)
def finding_timeline_on_save(sender, instance, created, **kwargs):
    # log that new finding was created
    if created:
        title = "created the finding"
        text = ""
        FindingTimeline.objects.create(
            title=title, text=text, finding=instance, user=instance.user
        )
        return


@receiver(signals.post_save, sender=Finding)
def init_scores(sender, instance, created, **kwargs):
    """initialize scores (e.g. CVSSBaseScore), if new finding is created

    Args:
        sender (_type_): _description_
        instance (_type_): _description_
        created (_type_): _description_
    """
    if created:
        CVSSBaseScore.objects.create(finding=instance)
        OWASPRiskRating.objects.create(finding=instance)
