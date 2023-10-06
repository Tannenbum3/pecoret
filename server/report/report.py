import datetime
from django.db.models import Count, Max, Q
from django.conf import settings
from backend.models import ProjectVulnerability, Finding, Host, WebApplication, Membership, ProjectScope
from backend.models.vulnerability import Severity
from pecoret.core.reporting import types as report_types
from pecoret.core.reporting.error import ReportError


class ErrorMixin:
    def check_finding_errors(self):
        # check finding errors
        for finding in Finding.objects.for_report(self.get_project()):
            if not finding.proof_text:
                error = ReportError("Missing proof!", f"#finding-{finding.pk}-proofs")
                self._add_error(error)
            if self.get_project().require_cvss_base_score and finding.cvssbasescore.is_incomplete:
                error = ReportError("Missing CVSS base score", f"#finding-{finding.pk}-title")
                self._add_error(error)


class PentestPDFReport(ErrorMixin, report_types.PentestPDFReport):

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
        context["members"] = Membership.objects.for_project(self.get_project()).for_report()
        context["scopes"] = ProjectScope.objects.for_project(self.get_project())
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

    def get_findings_count_for_asset(self, asset, severity=None):
        qs = asset.findings.exclude(exclude_from_report=True)
        if severity:
            qs = qs.filter(severity=Severity[severity].value)
        return qs.count()

    def check_report_errors(self):
        self.check_finding_errors()
        if not self.report_document.report.recommendation:
            error = ReportError("Missing recommendation!", "#executive-summary-recommendation")
            self._add_error(error)
        if not self.report_document.report.evaluation:
            error = ReportError("Missing evaluation!", "#executive-summary-evaluation")
            self._add_error(error)
        if not self.report_document.report.changehistory_set.count():
            error = ReportError("Change History missing!", "#change-history-table")
            self._add_error(error)


class SingleFindingPDFReport(ErrorMixin, report_types.SingleFindingPDFReport):
    def check_report_errors(self):
        self.check_finding_errors()


class AdvisoryMarkdownExport(report_types.AdvisoryMarkdownExport):
    pass


class AdvisoryPDFExport(report_types.AdvisoryPDFExport):

    def get_context(self):
        context = super().get_context()
        context["now"] = datetime.datetime.now().strftime("%B %d, %Y")
        return context


class VulnerabilityCSVReport(report_types.VulnerabilityCSVReport):
    pass


class PentestExcelReport(report_types.PentestExcelReport):
    pass
