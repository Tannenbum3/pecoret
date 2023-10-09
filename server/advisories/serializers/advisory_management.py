from pecoret.core.serializers import ValuedChoiceField, VulnerabilityTemplateIdField
from advisories.serializers.advisory import BaseAdvisorySerializer
from backend.serializers.vulnerability import VulnerabilityTemplateSerializer
from backend.models.advisory import AdvisoryStatusChoices
from .label import LabelSerializer
from .fields import LabelField


class AdvisoryAdvisoryManagementSerializer(BaseAdvisorySerializer):
    """
    an ``AdvisorySerializer`` which adds more fields used by the AdvisoryManagement
    """
    labels = LabelSerializer(many=True, read_only=True)
    vulnerability = VulnerabilityTemplateSerializer()
    status = ValuedChoiceField(choices=AdvisoryStatusChoices.choices)

    class Meta(BaseAdvisorySerializer.Meta):
        fields = BaseAdvisorySerializer.Meta.fields + [
            "status", "vulnerability", "cve_id", "is_draft",
            "date_disclosure", "date_planned_disclosure", "labels"
        ]


class AdvisoryManagementUpdateSerializer(BaseAdvisorySerializer):
    vulnerability = VulnerabilityTemplateSerializer(read_only=True)
    status = ValuedChoiceField(choices=AdvisoryStatusChoices.choices)
    labels = LabelField(serializer=LabelSerializer, many=True)
    vulnerability_id = VulnerabilityTemplateIdField(source="vulnerability_key")

    class Meta(BaseAdvisorySerializer.Meta):
        fields = BaseAdvisorySerializer.Meta.fields + [
            "status", "vulnerability", "cve_id", "is_draft",
            "date_disclosure", "date_planned_disclosure", "labels",
            "vulnerability_id"
        ]
