from backend.serializers.company import CompanySerializer
from backend.models import Company
from backend import permissions
from pecoret.core.viewsets import PeCoReTNoDestroyViewSet


class CompanyViewSet(PeCoReTNoDestroyViewSet):
    permission_classes = [
        permissions.GroupPermission(
            read_write_groups=[permissions.Groups.GROUP_MANAGEMENT],
            read_only_groups=[permissions.Groups.GROUP_PENTESTER],
        )
    ]
    queryset = Company.objects.none()
    search_fields = ["name"]
    serializer_class = CompanySerializer

    def get_queryset(self):
        return Company.objects.all()
