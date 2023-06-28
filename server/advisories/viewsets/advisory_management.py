from pecoret.core.viewsets import GenericViewSet
from pecoret.core import mixins
from backend.serializers.advisory import AdvisorySerializer
from backend.models import Advisory
from backend import permissions


class AdvisoryManagementInboxViewSet(mixins.ListModelMixin, GenericViewSet):
    permission_classes = [permissions.PRESET_GROUP_ADVISORY_MANAGEMENT]
    filter_class = None
    search_fields = ["product", "vendor_name", "internal_name", "vulnerability__vulnerability_id"]
    ordering_fields = ["advisory_id", "date_planned_disclosure", "date_created", "date_updated"]
    serializer_class = AdvisorySerializer

    def get_queryset(self):
        return Advisory.objects.for_advisory_management(include_user=None)
