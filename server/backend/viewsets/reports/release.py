from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import action
from django_q.tasks import async_task
from backend.serializers.reports.release import ReportReleaseSerializer
from backend.models.reports.report_release import ReportRelease, ReleaseType
from backend import permissions
from backend.permissions.report import ReportPermission
from backend.tasks.reporting import create_report_document_task
from pecoret.core.viewsets import PeCoReTNoUpdateViewSet


class ReportReleaseViewSet(PeCoReTNoUpdateViewSet):
    serializer_class = ReportReleaseSerializer
    queryset = ReportRelease.objects.none()
    filterset_class = None
    search_fields = []
    permission_classes = [permissions.PRESET_PENTESTER_OR_READONLY, ReportPermission]
    api_scope = "scope_all_projects"

    def get_queryset(self):
        qs = ReportRelease.objects.for_project(self.request.project).for_report(self.request.report)
        if self.action == "list":
            # exclude Preview documents from list view
            qs = qs.exclude(release_type=ReleaseType.PREVIEW)
        return qs

    def perform_create(self, serializer):
        instance = serializer.save(report=self.request.report)
        task_id = async_task(create_report_document_task, instance.pk)
        instance.task_id = task_id
        instance.save()

    @action(detail=True, methods=["get"])
    def download(self, request, pk=None, project=None, report=None):
        document = self.get_object()
        response = HttpResponse(
            document.compiled_source, content_type=document.content_type
        )
        filename = f"{document.name.lower()}-{ReleaseType(document.release_type).label.lower()}.{document.file_extension}"
        response["Content-Disposition"] = f'attachment; filename="{filename}"'
        return response

    @action(detail=False, methods=["get"])
    def preview_document(self, *args, **kwargs):
        """
        get the ReleaseType.PREVIEW document details
        :param args:
        :param kwargs:
        :return:
        """
        obj = self.request.report
        qs = ReportRelease.objects.for_project(self.request.project).for_report(obj).preview()
        if qs.exists():
            serializer = self.get_serializer(qs.get())
            data = serializer.data
        else:
            data = {}
        return Response(data)
