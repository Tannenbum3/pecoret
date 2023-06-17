from django.apps import AppConfig


class BackendConfig(AppConfig):
    """backend django application.
    here lives the core part of the application.
    """
    name = "backend"

    def ready(self):
        # keep it here instead of the recommended pecoret.__init__
        # otherwise gunicorn will fail to load because settings module is not yet ready
        # pylint: disable=unused-import
        # pylint: disable=import-outside-toplevel
        import pecoret.schema
        # patch translation
        from pecoret.core.reporting.translation import patch_django_translation
        patch_django_translation()
