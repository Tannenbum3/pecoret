from backend.serializers.company import CompanySerializer
from backend.models import Company
from pecoret.core import permissions
from pecoret.core.viewsets import PeCoReTNoDestroyViewSet


class CompanyViewSet(PeCoReTNoDestroyViewSet):
    queryset = Company.objects.none()
    search_fields = ["name"]
    serializer_class = CompanySerializer

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [
                permissions.GroupPermission(
                    read_write_groups=[],
                    read_only_groups=[
                        permissions.Groups.GROUP_MANAGEMENT, permissions.Groups.GROUP_PENTESTER
                    ]
                )
            ]
        if self.action == "create":
            return [
                permissions.GroupPermission(
                    read_write_groups=[
                        permissions.Groups.GROUP_MANAGEMENT
                    ],
                    read_only_groups=[]
                )
            ]
        return [
            permissions.CompanyPermission(
                read_write_groups=[
                    permissions.Groups.GROUP_PENTESTER,
                    permissions.Groups.GROUP_MANAGEMENT
                ],
                read_only_groups=[]
            )
        ]

    def get_queryset(self):
        return Company.objects.for_user(self.request.user)
