class PlainJinjaMixin:
    """mixin that just renders plain jinja templates"""

    def render_report(self):
        rendered_template = self.jinja_env.get_template(
            self.get_template_name()
        ).render(self.get_context())
        return rendered_template
