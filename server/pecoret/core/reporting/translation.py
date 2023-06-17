import os
from django.utils.translation.trans_real import DjangoTranslation
from django.conf import settings
from backend.models.report_templates import ReportTemplate


def patch_django_translation():
    """patch django translation to not use LOCALE_DIRS setting.
    Instead we use the path stored in the ``ReportTemplate``.

    Source: https://stackoverflow.com/a/60221067
    """
    def _add_local_translations(self):
        paths = ReportTemplate.objects.active().values_list("path", flat=True)
        for path in reversed(paths):
            locale_dir = os.path.join(path, "locale")
            translation = self._new_gnu_trans(locale_dir)
            self.merge(translation)
        self.merge(self._new_gnu_trans(str(settings.BASE_DIR / "locale")))

    DjangoTranslation._add_local_translations = _add_local_translations
