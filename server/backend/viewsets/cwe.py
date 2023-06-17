from backend.serializers.cwe import CWESerializer
from backend import permissions
from backend.models.cwe import CWE
from backend.filters.cwe import CWEFilter
from pecoret.core.viewsets import PeCoReTReadOnlyModelViewSet


class CWEViewSet(PeCoReTReadOnlyModelViewSet):
    serializer_class = CWESerializer
    permission_classes = [
        permissions.PRESET_GROUP_SUPERUSER_OR_READ_ONLY
    ]
    queryset = CWE.objects.all()
    search_fields = ["cwe_id", "name"]
    filterset_class = CWEFilter
