from backend.serializers.reports.change_history import ChangeHistorySerializer
from backend.models.reports.change_history import ChangeHistory
from backend import permissions
from backend.permissions.report import ReportPermission
from pecoret.core.viewsets import PeCoReTModelViewSet


class ChangeHistoryViewSet(PeCoReTModelViewSet):
    serializer_class = ChangeHistorySerializer
    queryset = ChangeHistory.objects.none()
    filterset_class = None
    search_fields = []
    api_scope = "scope_all_projects"
    permission_classes = [permissions.PRESET_PENTESTER_OR_READONLY, ReportPermission]

    def get_queryset(self):
        return ChangeHistory.objects.for_project(self.request.project).filter(
            report=self.request.report
        )

    def perform_create(self, serializer):
        serializer.save(report=self.request.report)
