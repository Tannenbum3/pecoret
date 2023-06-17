from pecoret.core.viewsets import PeCoReTModelViewSet
from backend.serializers.company_contact import CompanyContactSerializer
from backend.models.company_contact import CompanyContact
from backend.filters.company_contact import CompanyContactFilter
from backend import permissions


class CompanyContactViewSet(PeCoReTModelViewSet):
    permission_classes = [
        permissions.PRESET_GROUP_MANAGEMENT
    ]
    queryset = CompanyContact.objects.none()
    search_fields = ["first_name", "last_name"]
    filterset_class = CompanyContactFilter
    serializer_class = CompanyContactSerializer

    def get_queryset(self):
        return CompanyContact.objects.for_company(self.kwargs.get('company'))

    def perform_create(self, serializer):
        serializer.save(company_id=self.kwargs.get('company'))
