from pecoret.core.reporting import types as report_types
from .base import BaseDefaultReport


class SingleFindingPDFReport(BaseDefaultReport, report_types.SingleFindingPDFReport):
    def check_report_errors(self):
        self.check_finding_errors()
