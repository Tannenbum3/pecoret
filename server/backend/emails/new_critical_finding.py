from django.conf import settings
from .base import TemplatedBaseMail


class NewCriticalFindingEmail(TemplatedBaseMail):
    """notification for new critical findings in projects
    """
    template_name = "emails/projects/new_critical_finding.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context["url"] = settings.SITE_URLS.get("FINDING_DETAIL").format(**context)
        return context
