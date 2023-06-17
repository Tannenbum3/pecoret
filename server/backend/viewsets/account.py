from backend import permissions
from backend.models import Account
from backend.serializers.account import AccountSerializer
from pecoret.core.viewsets import PeCoReTModelViewSet


class AccountViewSet(PeCoReTModelViewSet):
    permission_classes = [permissions.PRESET_PENTESTER_OR_READONLY]
    queryset = Account.objects.none()
    filterset_class = None
    search_fields = ["username"]
    serializer_class = AccountSerializer

    def get_queryset(self):
        return Account.objects.for_project(self.request.project)

    def perform_create(self, serializer):
        serializer.save(project=self.request.project)
