from drf_spectacular.extensions import OpenApiSerializerFieldExtension
from drf_spectacular.contrib.django_filters import DjangoFilterExtension


class ValuedChoiceFieldFix(OpenApiSerializerFieldExtension):
    """fix for valuedchoicefield

    Args:
        OpenApiSerializerFieldExtension (_type_): _description_

    Returns:
        _type_: _description_
    """

    target_class = "pecoret.core.serializers.ValuedChoiceField"

    def map_serializer_field(self, auto_schema, direction):
        return {"type": "string", "enum": self.target.choices.values()}


class ValuedChoiceFilterFix(DjangoFilterExtension):
    """spectacular fix for custom choicefilter

    Args:
        DjangoFilterExtension (_type_): _description_

    Returns:
        _type_: _description_
    """

    target_class = "django_filters.rest_framework.DjangoFilterBackend"
    priority = 1
    match_subclasses = True

    def _get_explicit_filter_choices(self, filter_field):
        """override filter choices for values instead of key

        Args:
            filter_field (_type_): _description_

        Returns:
            _type_: _description_
        """
        if "choices" not in filter_field.extra:
            return None
        if callable(filter_field.extra["choices"]):
            # choices function may utilize the DB, so refrain from actually calling it.
            return []
        else:
            # only use values as valid choice filters
            return [v for _, v in filter_field.extra["choices"]]
