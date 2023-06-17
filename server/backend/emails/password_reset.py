from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from pecoret.core import utils
from .base import TemplatedBaseMail


class PasswordResetEmail(TemplatedBaseMail):
    """this template is used for the password reset mail
    """
    template_name = "emails/password_reset.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = context.get("user")
        context["uid"] = utils.encode_uid(user.pk)
        context["token"] = default_token_generator.make_token(user)
        context["url"] = settings.SITE_URLS.get("PASSWORD_RESET").format(**context)
        return context
