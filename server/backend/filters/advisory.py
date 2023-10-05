from django_filters import rest_framework as filters
from django_filters import widgets
from backend.models.advisory import Advisory, AdvisoryStatusChoices
from advisories.models.label import Label
from pecoret.core.utils.filters import ChoiceFilter


class AdvisoryFilter(filters.FilterSet):
    status = ChoiceFilter(choices=AdvisoryStatusChoices.choices)

    class Meta:
        model = Advisory
        fields = ["status", "is_draft"]


class InboxFilter(filters.FilterSet):
    status = ChoiceFilter(choices=AdvisoryStatusChoices.choices)
    # seems like `widgets.QueryArrayWidget` is required to have `labels[]=1` query syntax support
    labels = filters.ModelMultipleChoiceFilter(
        widget=widgets.QueryArrayWidget,
        queryset=Label.objects.all())

    class Meta:
        model = Advisory
        fields = ["status", "is_draft", "labels"]

    @property
    def qs(self):
        parent = super().qs
        return parent.for_advisory_management()
