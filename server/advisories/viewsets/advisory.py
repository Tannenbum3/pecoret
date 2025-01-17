from django.http.response import HttpResponse
from django.conf import settings
from rest_framework.decorators import action
from backend.models.advisory import Advisory, Roles
from advisories.serializers.advisory import (
    AdvisorySerializer,
    AdvisoryCreateSerializer,
    AdvisoryUpdateSerializer,
    AdvisoryDownloadSerializer
)
from advisories.serializers.timeline import AdvisoryTimelineSerializer
from backend.models import ReportTemplate
from backend.tasks.finding_export import export_advisory, export_advisory_markdown
from advisories.serializers.advisory_management import (
    AdvisoryAdvisoryManagementSerializer, AdvisoryManagementUpdateSerializer
)
from advisories.filters import AdvisoryFilter
from pecoret.core.viewsets import PeCoReTModelViewSet
from pecoret.core import permissions


class AdvisoryViewSet(PeCoReTModelViewSet):
    """Handles ``Advisory`` model.
    Here you can download markdown and pdf exports too.
    """

    queryset = Advisory.objects.none()
    filterset_class = AdvisoryFilter
    api_scope = "scope_advisories"
    search_fields = [
        "vulnerability__vulnerability_id",
        "product",
        "vendor_name",
        "internal_name",
    ]
    ordering_fields = [
        "advisory_id",
        "date_planned_disclosure",
        "date_created",
        "date_updated",
    ]
    serializer_class = AdvisorySerializer

    def get_permissions(self):
        """calculate required permissions based on the current action.

        Returns:
            _type_: _description_
        """
        if self.action == "list":
            return [
                permissions.GroupPermission(
                    read_write_groups=[
                        permissions.Groups.GROUP_PENTESTER,
                        permissions.Groups.GROUP_MANAGEMENT,
                        permissions.Groups.ADVISORY_MANAGEMENT,
                    ],
                    read_only_groups=[permissions.Groups.VENDOR],
                )()
            ]
        if self.action == "retrieve":
            return [
                permissions.AdvisoryPermission(
                    read_write_roles=[Roles.CREATOR],
                    read_only_roles=[Roles.READ_ONLY, Roles.VENDOR],
                )()
            ]
        if self.action in ["export_pdf", "export_markdown"]:
            return [
                permissions.AdvisoryPermission(
                    read_write_roles=[Roles.CREATOR],
                    read_only_roles=[Roles.READ_ONLY, Roles.VENDOR],
                )()
            ]
        if self.action == "create":
            return [
                permissions.GroupPermission(
                    read_write_groups=[
                        permissions.Groups.GROUP_PENTESTER,
                        permissions.Groups.GROUP_MANAGEMENT,
                        permissions.Groups.ADVISORY_MANAGEMENT,
                    ]
                )()
            ]
        return [
            permissions.AdvisoryPermission(
                read_write_roles=[Roles.CREATOR],
                read_only_roles=[Roles.READ_ONLY, Roles.VENDOR],
            )()
        ]

    def get_queryset(self):
        """The queryset depends on the current action and user group.
        The list action will only return ``Advisories`` for the current user.

        Returns:
            _type_: _description_
        """
        if self.action == "list":
            return Advisory.objects.for_user(self.request.user)
        if self.request.user.groups.filter(name="Advisory Management").exists():
            # allow advisory management users to update/delete/retrieve advisories (if not a draft)
            # otherwise, return only the user's advisories in list and retrieve views
            # advisory management users can get a list of submitted advisories from the "inbox" view.
            return Advisory.objects.for_advisory_management(
                include_user=self.request.user
            )
        return Advisory.objects.for_user(self.request.user)

    def perform_create(self, serializer):
        """save the serializer and populate the user field with the current user.

        Args:
            serializer (_type_): _description_
        """
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        """checks the current action and returns the correct serializer.

        Returns:
            ModelSerializer: A ModelSerializer class depending on the current action.
        """
        if self.action == "create":
            return AdvisoryCreateSerializer
        if self.action in ["list", "retrieve"]:
            if self.request.user.groups.filter(name="Advisory Management").exists():
                return AdvisoryAdvisoryManagementSerializer
            return AdvisorySerializer
        if self.action == "timeline":
            return AdvisoryTimelineSerializer
        if self.action in ["partial_update", "update"]:
            if self.request.user.groups.filter(name="Advisory Management").exists():
                return AdvisoryManagementUpdateSerializer
        return AdvisoryUpdateSerializer

    @action(detail=True, methods=["get"], serializer_class=AdvisoryDownloadSerializer)
    def export_pdf(self, request, **kwargs):
        """export the advisory details as PDF attachment

        Returns:
            HttpResponse: PDF Response
        """
        advisory = self.get_object()
        serializer = AdvisoryDownloadSerializer(data=request.GET)
        serializer.is_valid(raise_exception=True)
        if not serializer.data.get('template'):
            template = ReportTemplate.objects.get(name=settings.ADVISORY_TEMPLATE)
        else:
            template = serializer.data["template"]

        result = export_advisory(advisory, template)
        response = HttpResponse(result, content_type="application/pdf")
        filename = f"advisory_{advisory.pk}"
        response["Content-Disposition"] = f"attachment; filename={filename}.pdf"
        return response

    @action(detail=True, methods=["get"])
    # pylint: disable=unused-argument
    def export_markdown(self, _request, *args, **kwargs):
        """export advisory details as Markdown attachment

        Returns:
            HttpResponse: Response with file attachment
        """
        advisory = self.get_object()
        template = ReportTemplate.objects.get(name=settings.ADVISORY_TEMPLATE)
        result = export_advisory_markdown(advisory, template)
        response = HttpResponse(result, content_type="plain/text")
        filename = f"advisory_{advisory.pk}.md"
        response["Content-Disposition"] = f"attachment;filename={filename}"
        return response
