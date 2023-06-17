from collections import OrderedDict
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Subquery
from rest_framework import serializers
from backend.models.finding import ProjectVulnerability
from backend.models.membership import Roles
from backend.models.vulnerability import VulnerabilityTemplate
from backend.models.company import Company


class ValuedChoiceField(serializers.ChoiceField):
    """Custom choice field that allows inserts using value instead of key
    source: https://stackoverflow.com/a/54409752
    """

    def to_representation(self, value: int):
        if value == "" and self.allow_blank:
            return value
        return self._choices[value]

    def to_internal_value(self, data: str):
        # support inserts with the value
        if data == "" and self.allow_blank:
            return ""
        for key, value in self._choices.items():
            if value == data:
                return key
        self.fail("invalid_choice", input=data)


class PrimaryKeyRelatedField(serializers.RelatedField):
    """Source: https://github.com/encode/django-rest-framework/issues/5104#issuecomment-427774013
    a primarykeyrelatedfield that uses the object instance on read, but PK for write as normal.
    """

    def __init__(self, **kwargs):
        self.serializer = kwargs.pop("serializer")
        self.serializer_kwargs = kwargs.pop("serializer_kwargs", {})
        if self.serializer and "queryset" not in kwargs and not kwargs.get("read_only"):
            kwargs["queryset"] = self.serializer.Meta.model.objects.all()
        self.pk_field = serializers.PrimaryKeyRelatedField(**kwargs)
        super().__init__(**kwargs)

    def to_representation(self, value, pk=False):
        if pk:
            # workaround: https://github.com/encode/django-rest-framework/issues/5104
            # when pk is true you should return a string or string-convertible value
            return value.id
        # here you can return whatever you want as per your serializer
        return self.serializer(
            value, context=self.context, read_only=True, **self.serializer_kwargs
        ).data

    def get_choices(self, cutoff=None):
        # workaround: https://github.com/encode/django-rest-framework/issues/5104
        queryset = self.get_queryset()
        if queryset is None:
            return {}

        if cutoff is not None:
            queryset = queryset[:cutoff]

        return OrderedDict(
            [
                (
                    self.to_representation(item, pk=True),  # I added pk=true here
                    self.display_value(item),
                )
                for item in queryset
            ]
        )

    def to_internal_value(self, data):
        try:
            return self.get_queryset().get(pk=data)
        except ObjectDoesNotExist:
            self.pk_field.fail("does_not_exist", pk_value=data)
        except (TypeError, ValueError):
            self.pk_field.fail("incorrect_type", data_type=type(data).__name__)


class AssetField(serializers.DictField):
    default_error_messages = {
        "does_not_exist": 'Asset with this primary key and type does not exist.',
        "incorrect_type": 'Invalid asset type.',
        "incorrect_value": 'Incorrect value. Got error "{value}".',
        "malformed": 'DictField is malformed. Requires "type" and "pk" field.'
    }

    def __init__(self, **kwargs):
        self.serializers = kwargs.pop("serializers")
        super().__init__(**kwargs)

    def to_representation(self, value):
        serializer = self.serializers[value.asset_type].__class__
        return serializer(value, context=self.context).data

    def to_internal_value(self, data):
        if "type" not in data or "pk" not in data:
            self.fail("malformed")
        try:
            return self.get_queryset(data["type"]).get(pk=data["pk"])
        except ObjectDoesNotExist:
            self.fail("does_not_exist")
        except TypeError:
            self.fail("incorrect_type")
        except ValueError as error:
            self.fail("incorrect_value", value=str(error))

    def get_queryset(self, asset_type):
        if asset_type not in self.serializers:
            raise TypeError("unknown asset type")
        Asset = self.serializers[asset_type].Meta.model
        return Asset.objects.all()


class ProjectFilteredPrimaryKeyRelatedField(PrimaryKeyRelatedField):
    """field that filters relations for a project.
    model must have a queryset `for_project` method.
    """

    def get_queryset(self):
        return self.serializer.Meta.model.objects.for_project(
            self.context["request"].project
        )


class NonDraftAdvisoryPrimaryKeyRelatedField(PrimaryKeyRelatedField):
    def get_queryset(self):
        return self.serializer.Meta.model.objects.for_advisory_management()


class ProjectAssetField(AssetField):
    def get_queryset(self, *args):
        return super().get_queryset(*args).for_project(self.context["request"].project)


class ReportAuthorRelatedField(PrimaryKeyRelatedField):
    # required to only allow defined roles as report authors
    def get_queryset(self):
        allowed_author_roles = [Roles.PROJECT_LEADER, Roles.CONTRIBUTOR, Roles.OWNER]
        return (
            super()
            .get_queryset()
            .filter(
                membership__role__in=allowed_author_roles,
                membership__project=self.context["request"].project,
            )
        )


class ProjectVulnerabilityIdField(serializers.Field):
    default_error_messages = {
        "invalid_vulnerability_id": "vulnerability_id is not valid."
    }

    def to_representation(self, value):
        return value[1]

    # pylint: disable=inconsistent-return-statements
    def to_internal_value(self, data):
        key = [self.context["request"].project.pk, data]
        if ProjectVulnerability.objects.validate_key(*key):
            return key
        self.fail("invalid_vulnerability_id")


class VulnerabilityTemplateIdField(serializers.Field):
    default_error_messages = {
        "invalid_vulnerability_id": "vulnerability_id is not valid."
    }

    def to_representation(self, value):
        return value

    # pylint: disable=inconsistent-return-statements
    def to_internal_value(self, data):
        if VulnerabilityTemplate.objects.filter(vulnerability_id=data).exists():
            return data
        self.fail("invalid_vulnerability_id")


class CompanyScopedPrimaryKeyRelatedField(PrimaryKeyRelatedField):
    def get_queryset(self):
        project = self.context["request"].project
        return self.serializer.Meta.model.objects.for_company(
            Subquery(
                Company.objects.filter(project=project).values(
                    "pk"
                )
            )
        )
