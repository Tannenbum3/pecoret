from rest_framework import serializers
from checklists.models import Checklist, AssetChecklist
from backend.serializers.assets.web_application import WebApplicationSerializer
from backend.serializers.assets.host import HostSerializer
from backend.serializers.assets.service import MinimalServiceSerializer
from backend.serializers.assets.mobile_application import MobileApplicationSerializer
from backend.models import Host, Service, MobileApplication, WebApplication
from pecoret.core.serializers import AssetField


class ChecklistIdField(serializers.Field):
    default_error_messages = {"invalid_id": "Invalid checklist_id"}

    def to_representation(self, value):
        return value

    def to_internal_value(self, data):
        if Checklist.objects.filter(checklist_id=data).exists():
            return data
        self.fail("invalid_id")


class ChecklistSerializer(serializers.ModelSerializer):
    # categories = CategorySerializer(many=True, read_only=True)

    class Meta:
        model = Checklist
        fields = [
            "pk",
            "name",
            "checklist_id",
            # "categories"
        ]


ASSET_SERIALIZERS = {
    "web_application": WebApplicationSerializer(WebApplication.objects.all()),
    "host": HostSerializer(Host.objects.all()),
    "service": MinimalServiceSerializer(Service.objects.all()),
    "mobile_application": MobileApplicationSerializer(MobileApplication.objects.all()),
}


class AssetChecklistSerializer(ChecklistSerializer):
    asset = AssetField(serializers=ASSET_SERIALIZERS)
    # categories = AssetCategorySerializer(many=True, read_only=True)

    class Meta:
        model = AssetChecklist
        fields = ChecklistSerializer.Meta.fields + ["asset"]


class AssetChecklistCreateSerializer(AssetChecklistSerializer):
    checklist_id = ChecklistIdField()

    class Meta:
        model = AssetChecklist
        fields = ["checklist_id", "asset"]

    def create(self, validated_data):
        return AssetChecklist.objects.create_from_checklist(**validated_data)
