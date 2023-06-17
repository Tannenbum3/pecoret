from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from pecoret.core import utils
from .base import TemplatedBaseMail


class ActivationEmail(TemplatedBaseMail):
    """mail template for the activiation email
    """
    template_name = "emails/activation.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        user = context.get("user")
        context["username"] = user.username
        context["uid"] = utils.encode_uid(user.pk)
        context["token"] = default_token_generator.make_token(user)
        context["url"] = settings.SITE_URLS.get("ACTIVATION").format(**context)
        return context
