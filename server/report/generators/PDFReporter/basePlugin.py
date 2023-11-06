import yaml
import os
from pathlib import Path
from weasyprint import HTML, CSS
from jinja2 import Environment, PackageLoader, select_autoescape
import markdown
from playwright.sync_api import sync_playwright


# Could be usefull to standarize the context of a report
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

class BaseReporter():
    """
    Base peporter plugin
    """

    NAME = "BaseReporter" # Display Name of the reporter
    DESCRIPTION = "Defines a Plugin"

    # Describe all options available to the user and set default values
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
        },
        "allow_js": {
            "description": "Allow JavaScript in templates",
            "default": False
        },
        "highlight_engine": {
            "description": "Select a highlighting engine. Highlight.js requires allow_js = True",
            "default": str(Path(__file__).parent.resolve() / "conf/colors.yml")
        }
    }

    def __init__(self, context, config=None):
        self.config = config
        self.context = context
        self.config = {key: config.get(key, self.options[key]['default']) for key in self.config}
        # TODO: Create a shared templates dir which all reporter can access?
        # This way its possible to completly decouple the generation strategy from the design
        # same for cscc and so on
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
        if not self.config['allow_js']:
            html = self._execute_js(html)
        return html

    def _execute_js(self, html):
        with sync_playwright() as p:
            browser = p.chromium.launch()
            context = browser.new_context()
            page = context.new_page()
            page.set_content(html)
            executed_html_content = page.content()
            browser.close()
            return executed_html_content

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
