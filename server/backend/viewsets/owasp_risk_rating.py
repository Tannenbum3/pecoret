from backend.serializers.owasp_risk_rating import OWASPRiskRatingSerializer
from backend.models.owasp_risk_rating import OWASPRiskRating
from pecoret.core.viewsets import PeCoReTListUpdateRetrieveModelViewSet
from pecoret.core import permissions


class OWASPRiskRatingViewSet(PeCoReTListUpdateRetrieveModelViewSet):
    queryset = OWASPRiskRating.objects.none()
    serializer_class = OWASPRiskRatingSerializer
    api_scope = "scope_all_projects"
    permission_classes = [
        permissions.PRESET_PENTESTER_OR_READONLY,
        permissions.FindingPermission
    ]

    def get_queryset(self):
        return OWASPRiskRating.objects.for_project(self.request.project)

    def list(self, request, *args, **kwargs):
        """has a 1-1 relation with finding.
        no listing here, return single instance
        """
        self.lookup_field = "finding"
        self.lookup_url_kwarg = "finding"
        return self.retrieve(request)
