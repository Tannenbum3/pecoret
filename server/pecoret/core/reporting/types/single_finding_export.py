from django.core.exceptions import ImproperlyConfigured
from pecoret.core.utils.markdown import bleach_md
from .base import ProjectRelatedReportType
from .mixins.pdf import PDFExportMixin


class SingleFindingPDFReport(PDFExportMixin, ProjectRelatedReportType):
    """report for a exporting a single finding to PDF"""

    content_type = "application/pdf"
    file_extension = "pdf"
    default_title = "Finding Export"
    template_name = "single_finding_export.html"

    def __init__(self, *args, **kwargs):
        if "finding" not in kwargs:
            raise ImproperlyConfigured
        self.finding = kwargs["finding"]
        super().__init__(*args, **kwargs)

    def get_project(self):
        return self.finding.project

    def get_context(self):
        context = {"finding": self.finding, "report_helpers": {"bleach_md": bleach_md}}
        return context

    def post_processing(self, *args, **kwargs):
        pass

    def generate(self):
        """generated the report by doing pre processing, rendering and post processing steps.

        Returns:
            tuple: True and string if report was created
        """
        self.pre_processing()
        rendered_report = self.render_report()
        self.post_processing(rendered_report=rendered_report)
        return rendered_report
