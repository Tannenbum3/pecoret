from backend import permissions
from backend.permissions.finding import FindingPermission
from backend.serializers.finding_comment import FindingCommentSerializer
from backend.models import FindingComment
from pecoret.core.viewsets import PeCoReTNoDestroyViewSet


class FindingCommentViewSet(PeCoReTNoDestroyViewSet):
    permission_classes = [permissions.PRESET_PENTESTER_OR_READONLY, FindingPermission]
    queryset = FindingComment.objects.none()
    serializer_class = FindingCommentSerializer
    api_scope = "scope_all_projects"

    def get_queryset(self):
        return FindingComment.objects.for_project(self.request.project).for_finding(
            self.request.finding
        )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, finding=self.request.finding)
