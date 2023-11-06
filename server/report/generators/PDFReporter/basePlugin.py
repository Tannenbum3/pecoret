import yaml
import os
from pathlib import Path
from weasyprint import HTML, CSS
from jinja2 import Environment, PackageLoader, select_autoescape


class ReportContext:
    def __init__(self, remport_name, filename, company, members, scopes, vulnerabilities, findings, parts, errors):
        self.report_name = report_name
        self.filename = filename
        self.company = company
        self.members = members
        self.scopes = scopes
        self.vulnerabilities = vulnerabilities
        self.findings = findings
        self.findings = parts
        self.errors = errors

    def to_dict(self):
        return vars(self)

class PDFReporter():
    """
    Simple PDF Report plugin
    """

    NAME = "PDFReporter"
    DESCRIPTION = "Create a PDF report"

    options = {
        "template_parts_dir": {
            "description": "Directory containing HTML template parts",
            "default": str(Path(__file__).parent.resolve() / "templates/pages")
        },
        "report_template": {
            "description": "Path to the main HTML template",
            "default": str(Path(__file__).parent.resolve() / "templates/pentest_report")
        },
        "css_dir": {
            "description": "Directory containing CSS files",
            "default": str(Path(__file__).parent.resolve() / "templates/scss")
        },
        "colors": {
            "description": "Path to color configuration",
            "default": str(Path(__file__).parent.resolve() / "conf/colors.yml")
        }
    }

    def __init__(self, context, config=None):
        self.config = config
        self.context = context
        self.config = {key: config.get(key, self.options[key]['default']) for key in self.config}
        self.jinja_env = Environment(
            loader=PackageLoader(self.NAME)
        )

    def _load_css(self):
        css_dir = Path(__file__).parent.resolve() / self.CSS_DIR
        return list(parts_dir.rglob("*.scss"))

    def get_parts(self):
        return list(Path(self.config).rglob("*.html"))
    

    def _md_to_html(md):
        return md

    def _preprocess(self):
        """
        Prepare the context for report generation
        """
        pass

    def _postprocess(self, html):
        """
        Postprocess the HTML representation of the report
        """
        return html

    def generate(self):
        self._preprocess()
        report_content_html = ''
        for part in context['report_parts']:
            report_content_html += self._render_part(part)
        template = self.jinja_env.get_template(self.REPORT_TEMPLATE)
        report_html = template.render(report_content_html=report_content_html)
        report_html = self._postprocess(report_html)
        html = HTML(string=report_html) 
        html.write_pdf(target=self.config['filename'], stylesheets=self._load_css())

    def _render_part(self, part):
        template = self.jinja_env.get_template(f"{self.TEMPLATE_DIR}/{part}")
        return template.render(self.context.to_dict)
