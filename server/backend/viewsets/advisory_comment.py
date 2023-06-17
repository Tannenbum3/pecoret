from backend import permissions
from backend.models.advisory_comment import AdvisoryComment
from backend.models.advisory_membership import Roles
from backend.serializers.advisory_comment import AdvisoryCommentSerializer
from pecoret.core.viewsets import PeCoReTModelViewSet


class AdvisoryCommentViewSet(PeCoReTModelViewSet):
    """manage advisory comments"""

    queryset = AdvisoryComment.objects.none()
    permission_classes = [
        permissions.AdvisoryPermission(
            read_write_roles=[Roles.CREATOR, Roles.VENDOR],
            read_only_roles=[Roles.READ_ONLY],
        )
    ]
    serializer_class = AdvisoryCommentSerializer

    def get_queryset(self):
        qs = AdvisoryComment.objects.for_advisory(self.request.advisory)
        if self.action in ["list", "retrieve"]:
            return qs
        return qs.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(advisory=self.request.advisory, user=self.request.user)
