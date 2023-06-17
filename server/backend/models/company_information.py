from django.db import models
from django.core.exceptions import ValidationError
from pecoret.core.models import TimestampedModel, PeCoReTBaseModel


class CompanyInformationQuerySet(models.QuerySet):
    def for_company(self, company):
        return self.filter(company=company)


class CompanyInformation(TimestampedModel, PeCoReTBaseModel):
    objects = CompanyInformationQuerySet.as_manager()
    company = models.ForeignKey('backend.Company', on_delete=models.PROTECT)
    user = models.ForeignKey('backend.User', null=True, blank=True, on_delete=models.SET_NULL)
    text = models.TextField()

    def clean(self):
        if self.pk:
            if CompanyInformation.objects.get(pk=self.pk).company is not self.company:
                raise ValidationError({"company": "Company cannot be changed"})
        return super().clean()
