from backend.models import ProjectToken
from backend.serializers.project_token import ProjectTokenSerializer
from backend import permissions
from pecoret.core.viewsets import PeCoReTModelViewSet


class ProjectTokenViewSet(PeCoReTModelViewSet):
    serializer_class = ProjectTokenSerializer
    queryset = ProjectToken.objects.none()
    api_scope = None
    permission_classes = [permissions.PRESET_PENTESTER_OR_READONLY]

    def get_queryset(self):
        return ProjectToken.objects.for_project(self.request.project).filter(
            user=self.request.user
        )

    def perform_create(self, serializer):
        serializer.save(project=self.request.project, user=self.request.user)
