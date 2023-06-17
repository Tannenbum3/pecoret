from django_filters import rest_framework as filters
from pecoret.core.utils.filters import ChoiceFilter
from backend.models.project import Project, ProjectStatus


class ProjectFilter(filters.FilterSet):
    status = ChoiceFilter(choices=ProjectStatus.choices)

    class Meta:
        model = Project
        fields = ["status"]
