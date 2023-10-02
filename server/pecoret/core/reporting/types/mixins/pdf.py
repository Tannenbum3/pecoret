import os
import weasyprint
import sass
from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration


class PDFExportMixin:
    """mixin that exports html reports into PDF using weasyprint"""

    content_type = "application/pdf"
    file_extension = "pdf"
    css_files = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.font_config = FontConfiguration()

    def get_css_files(self):
        return self.css_files.copy()

    def get_stylesheets(self):
        css_paths = []
        for css in self.get_css_files():
            new_css_path = os.path.join(self.report_template.template_path, css)
            css_paths.append(new_css_path)
        # append sass files
        sass_path = os.path.join(self.report_template.template_path, "scss/main.scss")
        if os.path.exists(sass_path):
            compiled_scss = sass.compile(filename=sass_path, output_style="compressed")
            css_paths.append(
                CSS(
                    string=compiled_scss,
                    font_config=self.font_config,
                    url_fetcher=self.url_fetcher,
                )
            )
        return css_paths

    def url_fetcher(self, url, *args, **kwargs):
        if url.startswith("file://"):
            media_name = url.replace("file://", "")
            media_path = os.path.join(self.report_template.template_path, media_name)
            return {"file_obj": open(media_path, "rb")}
        return weasyprint.default_url_fetcher(url, *args, **kwargs)

    def render_report(self):
        rendered_template = self.jinja_env.get_template(
            self.get_template_name()
        ).render(self.get_context())
        weasy_html = HTML(string=rendered_template, url_fetcher=self.url_fetcher)
        weasy_pdf = weasy_html.write_pdf(
            stylesheets=self.get_stylesheets(), font_config=self.font_config,
            optimize_images=True  # Required to prevent weasyprint crashes in >=v59
        )
        return weasy_pdf
