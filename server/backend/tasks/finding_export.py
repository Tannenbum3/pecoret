from pecoret.core.reporting.loader import RenderableLoader


def export_single_finding(finding, template):
    # pylint: disable=invalid-name
    loader = RenderableLoader(template)
    RenderableReport = loader.load_template_class("SingleFindingPDFReport")
    result = RenderableReport(loader.report_template, None, finding=finding).generate()
    return result


def export_advisory(advisory, template):
    # pylint: disable=invalid-name
    loader = RenderableLoader(template)
    RenderableReport = loader.load_template_class("AdvisoryPDFExport")
    result = RenderableReport(
        loader.report_template, None, advisory=advisory
    ).generate()
    return result


def export_advisory_markdown(advisory, template):
    # pylint: disable=invalid-name
    loader = RenderableLoader(template)
    RenderableReport = loader.load_template_class("AdvisoryMarkdownExport")
    result = RenderableReport(
        loader.report_template, None, advisory=advisory
    ).generate()
    return result
