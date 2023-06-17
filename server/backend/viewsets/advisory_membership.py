from django_q.tasks import async_task
from backend.models.advisory_membership import AdvisoryMembership
from backend import permissions
from backend.tasks import mail
from backend.models.advisory_membership import Roles
from backend.serializers.advisory_membership import (
    AdvisoryMembershipSerializer,
    AdvisoryMembershipCreateSerializer,
)
from pecoret.core.viewsets import PeCoReTNoUpdateViewSet


class AdvisoryMembershipViewSet(PeCoReTNoUpdateViewSet):
    queryset = AdvisoryMembership.objects.none()
    permission_classes = [
        permissions.AdvisoryPermission(
            read_only_roles=[Roles.CREATOR, Roles.READ_ONLY, Roles.VENDOR]
        )
    ]

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return AdvisoryMembershipSerializer
        return AdvisoryMembershipCreateSerializer

    def get_queryset(self):
        return AdvisoryMembership.objects.for_advisory(self.request.advisory)

    def perform_create(self, serializer):
        instance = serializer.save(advisory=self.request.advisory)
        context = {
            "advisoryId": self.request.advisory.pk,
            "vendor_name": self.request.advisory.vendor_name,
        }
        async_task(mail.send_advisory_shared_mail, context, instance.user.email)
