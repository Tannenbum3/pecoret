from backend import permissions
from backend.models.advisory_timeline import AdvisoryTimeline
from backend.models.advisory_membership import Roles
from backend.serializers.advisory_timeline import AdvisoryTimelineSerializer
from pecoret.core.viewsets import PeCoReTModelViewSet


class AdvisoryTimelineViewSet(PeCoReTModelViewSet):
    """ViewSet of the AdvisoryTimeline.
    CRUD Methods.

    Returns:
        _type_: _description_
    """

    queryset = AdvisoryTimeline.objects.none()
    permission_classes = [
        permissions.AdvisoryPermission(
            read_write_roles=[Roles.CREATOR],
            read_only_roles=[Roles.READ_ONLY, Roles.VENDOR],
        )
    ]
    serializer_class = AdvisoryTimelineSerializer

    def get_queryset(self):
        return AdvisoryTimeline.objects.for_advisory(self.request.advisory)

    def perform_create(self, serializer):
        serializer.save(advisory=self.request.advisory)
