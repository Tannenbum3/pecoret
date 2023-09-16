from django.http import FileResponse
from rest_framework.decorators import action
from pecoret.core import permissions
from pecoret.core.viewsets import PeCoReTModelViewSet
from backend.models.finding_attachment import FindingImageAttachment
from backend.serializers.finding_attachment import FindingImageAttachmentSerializer


class FindingImageAttachmentViewSet(PeCoReTModelViewSet):
    queryset = FindingImageAttachment.objects.none()
    search_fields = ["caption"]
    api_scope = "scope_all_projects"
    serializer_class = FindingImageAttachmentSerializer
    permission_classes = [
        permissions.PRESET_PENTESTER_OR_READONLY,
        permissions.FindingPermission
    ]

    def get_queryset(self):
        return FindingImageAttachment.objects.for_project(self.request.project).for_finding(self.request.finding)

    def perform_create(self, serializer):
        serializer.save(finding=self.request.finding)

    @action(methods=['get'], detail=True)
    def preview(self, *args, **kwargs):
        instance = self.get_object()
        file_handle = instance.image.open()

        # send file
        response = FileResponse(file_handle)
        return response
