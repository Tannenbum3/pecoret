from pecoret.core.viewsets import PeCoReTModelViewSet
from pecoret.core import permissions
from backend.models.project_command import ProjectCommand
from backend.serializers.project_command import ProjectCommandSerializer


class ProjectCommandViewSet(PeCoReTModelViewSet):
    permission_classes = [permissions.PRESET_PENTESTER_OR_READONLY]
    filterset_class = None
    api_scope = "scope_all_projects"
    search_fields = ["command", "output"]
    ordering_fields = ["date_run"]
    serializer_class = ProjectCommandSerializer
    queryset = ProjectCommand.objects.none()

    def get_queryset(self):
        return ProjectCommand.objects.for_project(self.request.project)

    def perform_create(self, serializer):
        serializer.save(project=self.request.project, user=self.request.user)
