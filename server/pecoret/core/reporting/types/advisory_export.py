from django.core.exceptions import ImproperlyConfigured
from pecoret.reporting.mixins import PDFMixin
from .base import BaseReportType


class AdvisoryMarkdownExport(BaseReportType):
    content_type = "text/plain"
    file_extension = "md"
    default_title = ""
    template_file = "advisory.md"

    def __init__(self, *args, **kwargs):
        if "advisory" not in kwargs:
            raise ImproperlyConfigured
        super().__init__(*args, **kwargs)
        self.advisory = kwargs["advisory"]

    def get_context(self):
        context = super().get_context()
        context["advisory"] = self.advisory
        return context

    def render_report(self):
        return self.render_to_string(self.get_context())


class AdvisoryPDFExport(PDFMixin, BaseReportType):
    template_file = "advisory_export.html"

    def __init__(self, *args, **kwargs):
        if "advisory" not in kwargs:
            raise ImproperlyConfigured
        super().__init__(*args, **kwargs)
        self.advisory = kwargs["advisory"]

    def get_context(self):
        context = super().get_context()
        context["advisory"] = self.advisory
        return context

    def render_report(self):
        return self.render_pdf(self.get_context())
