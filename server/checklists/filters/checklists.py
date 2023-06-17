from django_filters import rest_framework as filters
from backend.models import WebApplication
from checklists.models import AssetChecklist
from pecoret.core.utils.filters import filter_model_by_project


class AssetChecklistFilter(filters.FilterSet):
    web_application = filters.ModelChoiceFilter(
        field_name="web_application", queryset=filter_model_by_project(WebApplication))

    class Meta:
        model = AssetChecklist
        fields = {
            "checklist_id": ["exact"]
        }
