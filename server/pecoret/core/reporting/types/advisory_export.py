from django.core.exceptions import ImproperlyConfigured
from .mixins.plain import PlainJinjaMixin
from .mixins.pdf import PDFExportMixin
from .base import BaseReportType


class AdvisoryMarkdownExport(PlainJinjaMixin, BaseReportType):
    content_type = "text/plain"
    file_extension = "md"
    default_title = ""
    template_name = "advisory.md"

    def __init__(self, *args, **kwargs):
        if "advisory" not in kwargs:
            raise ImproperlyConfigured
        super().__init__(*args, **kwargs)
        self.advisory = kwargs["advisory"]

    def get_context(self):
        context = super().get_context()
        context["advisory"] = self.advisory
        return context


class AdvisoryPDFExport(PDFExportMixin, BaseReportType):
    template_name = "advisory_export.html"

    def __init__(self, *args, **kwargs):
        if "advisory" not in kwargs:
            raise ImproperlyConfigured
        super().__init__(*args, **kwargs)
        self.advisory = kwargs["advisory"]

    def get_context(self):
        context = super().get_context()
        context["advisory"] = self.advisory
        return context
