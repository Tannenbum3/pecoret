from django.conf import settings
from .base import TemplatedBaseMail


class AdvisorySharedEmail(TemplatedBaseMail):
    """Email template for mail if an advisory was shared
    """
    template_name = "emails/advisories/shared.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context["url"] = settings.SITE_URLS.get("ADVISORY_DETAIL").format(**context)
        return context
