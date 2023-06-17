from backend import permissions
from backend.permissions.finding import FindingPermission
from backend.serializers.proof import ProofSerializer
from backend.models.proof import Proof
from pecoret.core.viewsets import PeCoReTModelViewSet


class ProofViewSet(PeCoReTModelViewSet):
    queryset = Proof.objects.none()
    search_fields = ["name"]
    ordering_fields = ["order"]
    serializer_class = ProofSerializer
    permission_classes = [permissions.PRESET_PENTESTER_OR_READONLY, FindingPermission]

    def get_queryset(self):
        return Proof.objects.for_project(self.request.project).for_finding(
            self.request.finding
        )

    def perform_create(self, serializer):
        serializer.save(finding=self.request.finding)
