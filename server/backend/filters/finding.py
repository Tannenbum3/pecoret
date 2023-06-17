from django_filters import rest_framework as filters
from pecoret.core.utils.filters import ChoiceFilter
from backend.models.finding import Finding, FindingStatus, Severity


class FindingFilter(filters.FilterSet):
    severity = ChoiceFilter(choices=Severity.choices)
    status = ChoiceFilter(choices=FindingStatus.choices)

    class Meta:
        model = Finding
        fields = ["status", "severity"]
