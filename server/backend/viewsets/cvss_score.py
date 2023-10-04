from backend.serializers.cvss_score import CVSSBaseScoreSerializer
from backend.models.cvss_score import CVSSBaseScore
from pecoret.core.viewsets import PeCoReTListUpdateRetrieveModelViewSet
from pecoret.core import permissions


class CVSSBaseScoreViewSet(PeCoReTListUpdateRetrieveModelViewSet):
    queryset = CVSSBaseScore.objects.none()
    serializer_class = CVSSBaseScoreSerializer
    api_scope = "scope_all_projects"
    permission_classes = [permissions.PRESET_PENTESTER_OR_READONLY, permissions.FindingPermission]

    def get_queryset(self):
        return CVSSBaseScore.objects.for_project(self.request.project)

    def list(self, request, *args, **kwargs):
        """CVSSBaseScore has a 1-1 relation with a finding.
        we do not require listing here. just return the single instance if exists.
        """
        self.lookup_url_kwarg = "finding"
        self.lookup_field = "finding"
        return self.retrieve(request)
