from checklists.models import AssetCategory
from checklists.serializers.category import AssetCategorySerializer
from checklists.filters.category import AssetCategoryFilter
from pecoret.core.viewsets import PeCoReTReadOnlyModelViewSet
from pecoret.core import permissions


class AssetCategoryViewSet(PeCoReTReadOnlyModelViewSet):
    queryset = AssetCategory.objects.none()
    permission_classes = [
        permissions.PRESET_PENTESTER_OR_READONLY
    ]
    serializer_class = AssetCategorySerializer
    filterset_class = AssetCategoryFilter
    search_fields = ["name", "assetitem__name"]

    def get_queryset(self):
        return AssetCategory.objects.for_project(self.request.project)
