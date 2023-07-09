from django_filters import rest_framework as filters
from checklists.models import AssetChecklist


class AssetChecklistFilter(filters.FilterSet):
    web_application = filters.NumberFilter(method="component_filter")
    host = filters.NumberFilter(method="component_filter")
    service = filters.NumberFilter(method="component_filter")
    mobile_application = filters.NumberFilter(method="component_filter")

    def component_filter(self, queryset, name, value):
        project = self.request.project
        return queryset.for_project(project).filter(**{name: value})

    class Meta:
        model = AssetChecklist
        fields = {
            "checklist_id": ["exact"]
        }
