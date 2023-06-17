from backend import permissions
from backend.serializers.advisory_proof import AdvisoryProofSerializer
from backend.models.advisory_proof import AdvisoryProof
from backend.models.advisory_membership import Roles
from pecoret.core.viewsets import PeCoReTModelViewSet


class AdvisoryProofViewSet(PeCoReTModelViewSet):
    queryset = AdvisoryProof.objects.none()
    permission_classes = [
        permissions.AdvisoryPermission(
            read_write_roles=[Roles.CREATOR],
            read_only_roles=[Roles.READ_ONLY, Roles.VENDOR],
        )
    ]
    serializer_class = AdvisoryProofSerializer
    filterset_backend = None
    search_fields = ["name"]
    ordering_fields = ["date_created", "name", "date_updated"]

    def get_queryset(self):
        return AdvisoryProof.objects.for_advisory(self.request.advisory)

    def perform_create(self, serializer):
        serializer.save(advisory=self.request.advisory)
