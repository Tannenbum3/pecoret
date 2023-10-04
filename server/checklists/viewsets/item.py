from checklists.models import AssetItem
from checklists.serializers.item import AssetItemSerializer, AssetItemUpdateSerializer
from checklists.filters.item import AssetItemFilter
from pecoret.core.viewsets import PeCoReTNoDestroyViewSet
from pecoret.core import permissions


class AssetItemViewSet(PeCoReTNoDestroyViewSet):
    queryset = AssetItem.objects.none()
    permission_classes = [
        permissions.PRESET_PENTESTER_OR_READONLY
    ]
    serializer_class = AssetItemSerializer
    filterset_class = AssetItemFilter
    search_fields = ["name"]

    def get_queryset(self):
        return AssetItem.objects.for_project(self.request.project)

    def get_serializer_class(self):
        if self.action in ["patch", "put"]:
            return AssetItemUpdateSerializer
        return AssetItemSerializer
