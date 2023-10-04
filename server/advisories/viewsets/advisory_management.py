from pecoret.core.viewsets import GenericViewSet
from pecoret.core import mixins
from pecoret.core import permissions
from backend.models import Advisory
from backend.filters.advisory import AdvisoryFilter
from advisories.serializers.advisory import AdvisoryAdvisoryManagementSerializer


class AdvisoryManagementInboxViewSet(mixins.ListModelMixin, GenericViewSet):
    permission_classes = [permissions.PRESET_GROUP_ADVISORY_MANAGEMENT]
    filterset_class = AdvisoryFilter
    search_fields = ["product", "vendor_name", "internal_name", "vulnerability__vulnerability_id"]
    ordering_fields = ["advisory_id", "date_planned_disclosure", "date_created", "date_updated"]
    serializer_class = AdvisoryAdvisoryManagementSerializer

    def get_queryset(self):
        return Advisory.objects.for_advisory_management(include_user=None)
