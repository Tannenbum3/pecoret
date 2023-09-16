from pecoret.core.viewsets import PeCoReTModelViewSet
from pecoret.core import permissions
from backend.serializers.assets.host import HostSerializer
from backend.models import Host


class HostViewSet(PeCoReTModelViewSet):
    permission_classes = [permissions.PRESET_PENTESTER_OR_READONLY]
    api_scope = "scope_all_projects"
    queryset = Host.objects.none()
    serializer_class = HostSerializer
    search_fields = ["ip", "dns"]

    def get_queryset(self):
        return Host.objects.for_project(self.request.project)

    def perform_create(self, serializer):
        serializer.save(project=self.request.project)
