from rest_framework import serializers
from backend.models import ProjectVulnerability
from backend.models import WebApplication, Host, Service, MobileApplication
from backend.models.finding import Finding, Severity, FindingStatus
from backend.serializers.assets.web_application import WebApplicationSerializer
from backend.serializers.assets.host import HostSerializer
from backend.serializers.assets.service import MinimalServiceSerializer
from backend.serializers.assets.mobile_application import MobileApplicationSerializer
from pecoret.core.serializers import (
    ValuedChoiceField,
    AssetField,
    ProjectVulnerabilityIdField,
    ProjectFilteredPrimaryKeyRelatedField,
)
from .vulnerability import ProjectVulnerabilitySerializer
from .account import AccountSerializer


ASSET_SERIALIZERS = {
    "web_application": WebApplicationSerializer(WebApplication.objects.all()),
    "host": HostSerializer(Host.objects.all()),
    "service": MinimalServiceSerializer(Service.objects.all()),
    "mobile_application": MobileApplicationSerializer(MobileApplication.objects.all()),
}


class FindingSerializer(serializers.ModelSerializer):
    vulnerability = ProjectVulnerabilitySerializer(
        ProjectVulnerability.objects.all(), read_only=True
    )
    severity = ValuedChoiceField(choices=Severity.choices)
    status = ValuedChoiceField(choices=FindingStatus.choices)
    asset = AssetField(serializers=ASSET_SERIALIZERS)
    internal_id = serializers.CharField(read_only=True)
    user_account = ProjectFilteredPrimaryKeyRelatedField(
        required=False, allow_empty=True, allow_null=True, serializer=AccountSerializer
    )

    class Meta:
        model = Finding
        fields = [
            "pk",
            "date_created",
            "date_updated",
            "vulnerability",
            "internal_id",
            "user_account",
            "recommendation",
            "severity",
            "status",
            "imported",
            "name",
            "finding_date",
            "authenticated_test",
            "needs_review",
            "asset",
            "retest_results",
            "date_retest",
            "exclude_from_report",
        ]


class FindingCopySerializer(FindingSerializer):
    class Meta:
        model = Finding
        fields = ["name"]
        read_only_fields = [
            "pk",
            "date_created",
            "date_updated",
            "vulnerability",
            "internal_id",
            "recommendation",
            "severity",
            "status",
            "authenticated_test",
            "needs_review",
            "asset",
            "vulnerability_id",
        ]


class FindingCreateSerializer(FindingSerializer):
    vulnerability_id = ProjectVulnerabilityIdField(source="vuln_key")
    severity = ValuedChoiceField(choices=Severity.choices, required=False)

    def create(self, validated_data):
        return Finding.objects.create_from_template(**validated_data)

    class Meta(FindingSerializer.Meta):
        fields = FindingSerializer.Meta.fields + ["vulnerability_id"]


class FindingAsAdvisorySerializer(serializers.Serializer):
    product = serializers.CharField()
    vendor_url = serializers.URLField()
    vendor_name = serializers.CharField()
    affected_versions = serializers.CharField()
