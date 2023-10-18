from django.core.exceptions import ImproperlyConfigured
from pecoret.reporting.mixins import PDFMixin
from .base import ProjectRelatedReportType


class SingleFindingPDFReport(PDFMixin, ProjectRelatedReportType):
    """report for a exporting a single finding to PDF"""

    content_type = "application/pdf"
    file_extension = "pdf"
    default_title = "Finding Export"
    template_file = "single_finding_export.html"

    def __init__(self, *args, **kwargs):
        if "finding" not in kwargs:
            raise ImproperlyConfigured
        self.finding = kwargs["finding"]
        super().__init__(*args, **kwargs)

    def get_project(self):
        return self.finding.project

    def get_context(self):
        context = super().get_context()
        context["finding"] = self.finding
        return context

    def post_processing(self, *args, **kwargs):
        pass

    def generate(self):
        """generated the report by doing pre-processing, rendering and post-processing steps.

        Returns:
            tuple: True and string if report was created
        """
        self.pre_processing()
        rendered_report = self.render_pdf(self.get_context())
        self.post_processing(rendered_report=rendered_report)
        return rendered_report
