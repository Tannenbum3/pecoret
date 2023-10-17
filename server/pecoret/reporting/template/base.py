import sys
from pathlib import Path
from django.utils import translation
from jinja2 import FileSystemLoader
from jinja2.sandbox import SandboxedEnvironment


class BaseTemplate:
    jinja_autoescape = True

    def __init__(self, report_template, *args, **kwargs):
        self.report_template = report_template
        self.jinja_loader = FileSystemLoader(self.template_path)
        self.jinja_env = SandboxedEnvironment(
            loader=self.jinja_loader,
            autoescape=self.jinja_autoescape,
            extensions=["jinja2.ext.i18n"],
        )
        self.enable_i18n()

    @property
    def template_dir(self):
        return Path(sys.modules[self.__module__].__file__).parent

    @property
    def template_path(self):
        path = self.template_dir / 'templates'
        return str(path)

    def enable_i18n(self):
        self.jinja_env.install_gettext_translations(translation)
        self.jinja_env.policies['ext.i18n.trimmed'] = True
        # self.jinja_env.filters['dynamic_trans'] = dynamic_trans

    def _activate_translation_lang(self, lang):
        translation.activate(lang)
