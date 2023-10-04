from checklists.models import Checklist, AssetChecklist
from checklists.serializers.checklist import (
    ChecklistSerializer,
    AssetChecklistSerializer,
    AssetChecklistCreateSerializer,
)
from checklists.filters.checklists import AssetChecklistFilter
from pecoret.core.viewsets import PeCoReTReadOnlyModelViewSet, PeCoReTNoUpdateViewSet
from pecoret.core import permissions


class ChecklistViewSet(PeCoReTReadOnlyModelViewSet):
    queryet = Checklist.objects.none()
    permission_classes = [
        permissions.GroupPermission(
            read_only_groups=[
                permissions.Groups.GROUP_MANAGEMENT,
                permissions.Groups.GROUP_PENTESTER,
            ]
        )
    ]
    search_fields = ["name", "checklist_id"]
    serializer_class = ChecklistSerializer

    def get_queryset(self):
        return Checklist.objects.all()


class AssetChecklistViewSet(PeCoReTNoUpdateViewSet):
    queryset = AssetChecklist.objects.none()
    filterset_class = AssetChecklistFilter
    search_fields = ["name"]
    permission_classes = [permissions.PRESET_PENTESTER_OR_READONLY]
    serializer_class = AssetChecklistSerializer

    def get_queryset(self):
        return AssetChecklist.objects.for_project(self.request.project)

    def get_serializer_class(self):
        if self.action == "create":
            return AssetChecklistCreateSerializer
        return AssetChecklistSerializer

    def perform_create(self, serializer):
        serializer.save(project=self.request.project)

    def perform_destroy(self, instance):
        instance.categories.all().delete()
        super().perform_destroy(instance)
