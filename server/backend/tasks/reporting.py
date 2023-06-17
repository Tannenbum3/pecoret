from backend.models.reports.report_release import ReportRelease
from backend.models.reports.report import ReportVariant
from pecoret.core.reporting.loader import RenderableLoader


def create_report_document_task(report_document_pk):
    report_document = ReportRelease.objects.get(pk=report_document_pk)
    # get the report variant (e.g. Pentest PDF)
    report_variant = ReportVariant(report_document.report.variant)
    loader = RenderableLoader(report_template=report_document.report.template)
    # pylint: disable=invalid-name
    RenderableReport = loader.load_template_class_for_variant(report_variant)
    result = RenderableReport(loader.report_template, report_document).generate()
    return result
