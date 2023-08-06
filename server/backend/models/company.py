from django.db import models
from .membership import Membership


class CompanyQuerySet(models.QuerySet):
    def for_project_ids(self, project_ids):
        return self.filter(project__pk__in=project_ids)

    def for_user(self, user):
        if user.groups.filter(name="Management").exists():
            return self.all()
        project_ids = list(Membership.objects.for_user(user).is_active().values_list("project", flat=True))
        return self.for_project_ids(project_ids)


class Company(models.Model):
    objects = CompanyQuerySet.as_manager()
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=256)
    street = models.CharField(max_length=256)
    zipcode = models.CharField(max_length=256)
    city = models.CharField(max_length=256)
    country = models.CharField(max_length=256)
    report_template = models.ForeignKey('backend.ReportTemplate', on_delete=models.PROTECT)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name
