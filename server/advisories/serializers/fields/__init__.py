from rest_framework import serializers
from pecoret.core.serializers import PrimaryKeyRelatedField
from advisories.models import Label


class LabelField(PrimaryKeyRelatedField):
    pass
