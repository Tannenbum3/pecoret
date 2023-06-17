from rest_framework import serializers
from backend.models.owasp_risk_rating import OWASPRiskRating


class OWASPRiskRatingSerializer(serializers.ModelSerializer):
    """we do not use valuedchoicefields here"""

    class Meta:
        model = OWASPRiskRating
        fields = [
            "skill_level",
            "motive",
            "opportunity",
            "size",
            "ease_of_discovery",
            "ease_of_exploit",
            "awareness",
            "intrusion_detection",
            "loss_of_availability",
            "loss_of_confidentiality",
            "loss_of_accountability",
            "loss_of_integrity",
            "financial_damage",
            "reputation_damage",
            "non_compliance",
            "privacy_violation",
            "pk",
            "overall_risk_severity",
            "likelihood_factors",
            "impact_factors"
        ]
        read_only_fields = [
            "pk",
            "overall_risk_severity",
            "likelihood_factors",
            "impact_factors",
        ]
