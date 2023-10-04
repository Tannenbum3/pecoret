from backend.serializers.finding_timeline import FindingTimelineSerializer
from backend.models import FindingTimeline
from pecoret.core.viewsets import PeCoReTReadOnlyModelViewSet
from pecoret.core import permissions


class FindingTimelineViewSet(PeCoReTReadOnlyModelViewSet):
    permission_classes = [permissions.PRESET_PENTESTER_OR_READONLY, permissions.FindingPermission]
    serializer_class = FindingTimelineSerializer
    search_fields = []
    api_scope = "scope_all_projects"
    queryset = FindingTimeline.objects.none()

    def get_queryset(self):
        return FindingTimeline.objects.for_project(self.request.project).for_finding(
            self.request.finding
        )
