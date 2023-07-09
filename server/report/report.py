import datetime
import io
import matplotlib.pyplot as plt
import matplotlib as mpl
from django.db.models import Count, Max, Q
from django.utils.html import format_html
from django.conf import settings
from backend.models import ProjectVulnerability, Finding, Host, WebApplication
from backend.models.vulnerability import Severity
from backend.models.finding import FindingStatus
from pecoret.core.reporting import types as report_types
from pecoret.core.reporting.error import ReportError


mpl.use("Agg")


class Chart:
    def __init__(self, project):
        self.plt = None
        self.project = project

    def get_html(self, plot):
        figure_file = io.StringIO()
        plot.savefig(figure_file, format="svg", transparent=True)
        plot.close("all")
        svg = "<svg" + figure_file.getvalue().split("<svg")[1]
        return format_html(
            '<img class="graph" src="data:image/svg+xml;utf8,{}" Z>', svg
        )

    def plot_severity_pie_chart(self, colors):
        if not Finding.objects.for_report(self.project).exists():
            return ""
        # TODO: make this more efficient
        values = [
            Finding.objects.for_report(self.project)
            .filter(~Q(status=FindingStatus.FIXED), severity=Severity.CRITICAL)
            .count(),
            Finding.objects.for_report(self.project)
            .filter(~Q(status=FindingStatus.FIXED), severity=Severity.HIGH)
            .count(),
            Finding.objects.for_report(self.project)
            .filter(~Q(status=FindingStatus.FIXED), severity=Severity.MEDIUM)
            .count(),
            Finding.objects.for_report(self.project)
            .filter(~Q(status=FindingStatus.FIXED), severity=Severity.LOW)
            .count(),
            Finding.objects.for_report(self.project)
            .filter(~Q(status=FindingStatus.FIXED), severity=Severity.INFORMATIONAL)
            .count(),
        ]
        fig, ax = plt.subplots(figsize=[6, 2.5])
        ax.pie(values, startangle=90, colors=colors)
        return self.get_html(plt)


class PentestPDFReport(report_types.PentestPDFReport):
    COLORS = ["#9c1720", "#d13c0f", "#e8971e", "#2075f5", "#059D1D"]

    def get_assets(self):
        assets = []
        assets += list(Host.objects.for_project(self.get_project()))
        assets += list(WebApplication.objects.for_project(self.get_project()))
        return assets

    def get_context(self):
        context = super().get_context()
        context["now"] = datetime.datetime.now().strftime("%B %d, %Y")
        context["REPORT_COMPANY_INFORMATION"] = settings.REPORT_COMPANY_INFORMATION
        context["findings"] = Finding.objects.for_report(self.get_project())
        return context

    def get_unique_vulnerabilities_by_severity(self):
        return (
            ProjectVulnerability.objects.for_project(project=self.get_project())
            .annotate(
                count=Count(
                    "finding__pk", distinct=True, filter=~Q(exclude_from_report=True)
                )
            )
            .annotate(finding_severity=Max("finding__severity"))
            .order_by("-finding__severity", "vulnerability_id")
            .filter(count__gt=0)
        )

    def get_vulnerabilities(self):
        return ProjectVulnerability.objects.for_project(
            project=self.get_project()
        ).filter(finding__is_null=False)

    def plot_severity_chart(self):
        return Chart(self.get_project()).plot_severity_pie_chart(self.COLORS)

    def get_errors(self):
        errors = []
        for finding in Finding.objects.for_report(self.get_project()):
            if not finding.proof_set.all():
                error = ReportError("Missing proof!", f"#finding-{finding.pk}-title")
                errors.append(error)
            if self.get_project().require_cvss_base_score and finding.cvssbasescore.is_incomplete:
                error = ReportError("Missing CVSS base score", f"#finding-{finding.pk}-title")
                errors.append(error)
        if not self.report_document.report.recommendation:
            error = ReportError("Missing recommendation!", "#management-summary-recommendation")
            errors.append(error)
        if not self.report_document.report.evaluation:
            error = ReportError("Missing evaluation!", "#management-summary-evaluation")
            errors.append(error)
        return errors

    def get_findings_count_for_asset(self, asset, severity=None):
        qs = asset.findings.exclude(exclude_from_report=True)
        if severity:
            qs = qs.filter(severity=Severity[severity].value)
        return qs.count()


class SingleFindingPDFReport(report_types.SingleFindingPDFReport):
    pass


class AdvisoryMarkdownExport(report_types.AdvisoryMarkdownExport):
    pass


class AdvisoryPDFExport(report_types.AdvisoryPDFExport):
    pass


class VulnerabilityCSVReport(report_types.VulnerabilityCSVReport):
    pass
