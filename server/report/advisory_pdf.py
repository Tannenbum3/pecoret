import datetime
from pecoret.core.reporting import types as report_types


class AdvisoryPDFExport(report_types.AdvisoryPDFExport):

    def get_context(self):
        context = super().get_context()
        context["now"] = datetime.datetime.now().strftime("%B %d, %Y")
        return context
