import cvss
from django.db import models


class AVChoices(models.IntegerChoices):
    NETWORK = 0, "N"
    ADJACENT_NETWORK = 1, "A"
    LOCAL = 2, "L"
    PHYSICAL = 3, "P"


class ACChoices(models.IntegerChoices):
    LOW = 0, "L"
    HIGH = 1, "H"


class UIChoices(models.IntegerChoices):
    NONE = 0, "N"
    REQUIRED = 1, "R"


class SChoices(models.IntegerChoices):
    UNCHANGED = 0, "U"
    CHANGED = 1, "C"


class NoneLowHighChoices(models.IntegerChoices):
    NONE = 0, "N"
    LOW = 1, "L"
    HIGH = 2, "H"


class CVSSBaseScoreQuerySet(models.QuerySet):
    def for_project(self, project):
        return self.filter(finding__project=project)


class CVSSBaseScore(models.Model):
    objects = CVSSBaseScoreQuerySet.as_manager()
    finding = models.OneToOneField("backend.Finding", on_delete=models.CASCADE)
    av = models.PositiveIntegerField(choices=AVChoices.choices, null=True)
    ac = models.PositiveIntegerField(choices=ACChoices.choices, null=True)
    pr = models.PositiveIntegerField(choices=NoneLowHighChoices.choices, null=True)
    ui = models.PositiveIntegerField(choices=UIChoices.choices, null=True)
    s = models.PositiveIntegerField(choices=SChoices.choices, null=True)
    a = models.PositiveIntegerField(choices=NoneLowHighChoices.choices, null=True)
    i = models.PositiveIntegerField(choices=NoneLowHighChoices.choices, null=True)
    c = models.PositiveIntegerField(choices=NoneLowHighChoices.choices, null=True)

    def __str__(self):
        return (
            f"AV:{self.get_av_display()}/AC:{self.get_ac_display()}/PR:{self.get_pr_display()}/UI:{self.get_ui_display()}"
            + f"/S:{self.get_s_display()}/A:{self.get_a_display()}/C:{self.get_c_display()}/I:{self.get_i_display()}"
        )

    @property
    def cvss31_vector(self):
        return "CVSS:3.1/" + str(self)

    @property
    def is_incomplete(self):
        if (
            self.av is None
            or self.ac is None
            or self.pr is None
            or self.ui is None
            or self.s is None
        ):
            return True
        if self.a is None or self.c is None or self.i is None:
            return True
        return False

    @property
    def cvss31_base_severity(self):
        if self.is_incomplete:
            return "Incomplete"
        return cvss.CVSS3(self.cvss31_vector).severities()[0]

    @property
    def cvss31_base_score(self):
        if self.is_incomplete:
            return "Incomplete"
        return cvss.CVSS3(self.cvss31_vector).scores()[0]

    class Meta:
        ordering = ["finding"]
