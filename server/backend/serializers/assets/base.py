from rest_framework import serializers
from backend.models.assets.base import Environment, AssetAccessibility
from pecoret.core.serializers import ValuedChoiceField


class BaseAssetSerializer(serializers.ModelSerializer):
    environment = ValuedChoiceField(choices=Environment.choices, required=False)
    accessible = ValuedChoiceField(choices=AssetAccessibility.choices, required=False)

    class Meta:
        fields = [
            "pk",
            "date_updated",
            "date_created",
            "accessible",
            "description",
            "environment",
            "display_name",
            "asset_type"
        ]
        read_only_fields = ["asset_type"]
