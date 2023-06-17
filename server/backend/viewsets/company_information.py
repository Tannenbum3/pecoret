from pecoret.core.viewsets import PeCoReTModelViewSet
from backend.models.company_information import CompanyInformation
from backend.serializers.company_information import CompanyInformationSerializer
from backend.filters.company_information import CompanyInformationFilter
from backend import permissions


class CompanyInformationViewSet(PeCoReTModelViewSet):
    queryset = CompanyInformation.objects.none()
    filterset_class = CompanyInformationFilter
    serializer_class = CompanyInformationSerializer
    permission_classes = [
        permissions.PRESET_GROUP_PENTESTER_MANAGEMENT
    ]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return CompanyInformation.objects.all()
